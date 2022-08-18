
from alert import Logger, Check, Message

from checks.services import checkIsUpdatedServices

loggerFile = "logger.json"
l = Logger(loggerFile=loggerFile)

message = Message(
    subject="Alert",
    body="Found slots",
)
check = Check(name="Slots",
        message = message,
        _check = checkIsUpdatedServices,
        )

checks = [check, check]

log = {'message':str(message),
       'checks': [str(x) for x in checks],
       }
l.add(log)
l.show()
