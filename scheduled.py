import argparse
import asyncio
from addy.db import Session
from addy.models.user import User
from addy.models.historicalwalletvalue import HistoricalWalletValue
from addy.models.scoreboard import Scoreboard
from addy.models.scoreboardrecord import ScoreboardRecord
import addy.commands.crypto.getters as getters


async def createscoreboard():

    with Session() as session:
        user_list = session.query(User).all()
        new_scoreboard = Scoreboard()
        for user in user_list:
            prev_wallet_balance = (
                session.query(HistoricalWalletValue)
                .filter_by(crypto_wallet_id=user.crypto_wallet_id)
                .order_by(HistoricalWalletValue._id.desc())
                .first()
            )
            if not prev_wallet_balance:
                print("skipped")
                continue
            wallet_balance = user.crypto_wallet.balance
            holding_total = await getters.tally_holdings(
                session, user, user.crypto_wallet.crypto_holdings
            )

            hwalletvalue = HistoricalWalletValue(
                crypto_wallet_id=user.crypto_wallet.id,
                usd_balance=wallet_balance,
                holdings_balance=holding_total["total"],
                total_balance=holding_total["total"] + wallet_balance,
            )
            score = hwalletvalue.total_balance - prev_wallet_balance.total_balance
            new_record = ScoreboardRecord(
                scoreboard=new_scoreboard,
                user=user,
                starting_wallet_balance=prev_wallet_balance,
                ending_wallet_balance=hwalletvalue,
                score=score,
            )
            session.add(hwalletvalue)
            session.add(new_record)
        session.add(new_scoreboard)
        session.commit()
        print("Scoreboard created succesfully")


async def main():

    parser = argparse.ArgumentParser(description="Process some integers.")

    parser.add_argument("command")
    arg = parser.parse_args()
    function_mapper = {"createscoreboard": createscoreboard}

    await function_mapper[arg.command]()


if __name__ == "__main__":
    asyncio.run(main())
