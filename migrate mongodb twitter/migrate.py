import pymongo
import logging
import sys
from sqlalchemy.exc import IntegrityError
from pymongo import MongoClient
from tweeply.models import TweeplyMessage, Credential, User, Database
from tweeply.utils import update_config

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

#MONGODB: USERNAME, PASSWORD, HOST, DB

if __name__ == '__main__':
    settings = update_config({})
    msettings = settings["MONGODB"]
    tsettings = settings["TWITTER"]
    mongoclient = MongoClient(msettings["HOST"])
    mongo = mongoclient[msettings['DB']]
    logger.debug("Connecting to {}/{} as {}:{}".format(
        msettings["HOST"],
        msettings["DB"],
        msettings.get("USERNAME", None),
        msettings.get("PASSWORD", None)))
    if "USERNAME" in msettings and "PASSWORD" in msettings:
        mongo.authenticate(msettings['USERNAME'], msettings['PASSWORD'])
    db = Database(settings)

    not_import = set(["garbage", "system.indexes"])
    collections = set(mongo.collection_names()) - not_import

    if "credentials" in collections:
        logger.info("Adding credentials")
        print("Adding credentials")
        collections.remove("credentials")
        for c in mongo["credentials"].find():
            logger.info("\tFound: %s", c)
            if "token" in c and "user" in c:
                if not db.query(Credential).filter_by(user=c["user"]).first():
                    cred = Credential(user=c["user"],
                                    access_token=c["token"][0],
                                    access_token_secret=c["token"][1],
                                    consumer_key=tsettings["CONSUMER_KEY"],
                                    consumer_secret=tsettings["CONSUMER_SECRET"]
                    )
                    db.add(cred)
        db.commit()

    if "users" in collections:
        logger.info("Adding users")
        collections.remove("users")
        for u in mongo["users"].find():
            logger.info("\tFound: %s", c)
            if "id" in u:
                del u["_id"]
                user = User(id=u["id"],
                            screen_name=u.get("screen_name", None),
                            raw=u)
                try:
                    db.merge(user)
                except IntegrityError:
                    pass
        db.commit()


    logger.info("Adding all messages")
    for cname in collections:
        collection = mongo[cname]
        sofar = 0
        skipped = 0
        #maxid = collection.find().sort("msgid", -1).limit(1)[0]["msgid"]
        #while maxid > 0:
            #chunk = list(collection.find({"msgid": {"$lt": maxid}}).sort("msgid",-1).limit(100))
            #maxid = chunk[-1]["msgid"]
        msgs = []
        for msg in  collection.find():
            msgs.append(msg)
            sofar += 1
            newmsg = TweeplyMessage(id=msg["msgid"],
                                    collection=msg["collection"],
                                    code=msg["code"],
                                    payload=msg["payload"],
                                    thread=msg.get("thread", 0),
                                    multipart=msg.get("multipart", False),
                                    stimestamp=msg.get("stimestamp", 0),
                                    rtimestamp=msg.get("rtimestamp", 0))
            try:
                db.add(newmsg)
                db.commit()
            except IntegrityError:
                db.rollback()
                skipped += 1
            sys.stdout.write('\r\t%s messages so far. %s skipped' % (sofar, skipped))
        #db.commit()
        sys.stdout.write('\r\t%s messages read' % sofar)
        added = db.query(TweeplyMessage).count()
        logger.info("Added %s messages", added)

