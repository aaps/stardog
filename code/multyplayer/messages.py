import legume


MSGID = legume.messages.BASE_MESSAGETYPEID_USER
NETWORK_INTERVAL = 0.033333333
PORT = 6666



class PlanetUpdate(legume.messages.BaseMessage):
    MessageTypeID = MSGID+1
    MessageValues = {
        'entity_id' : 'int',
        'frame_number' : 'int',
        'name' : 'string 32',
        'x' : 'int',
        'y' : 'int',
        'dx' : 'int',
        'dy' : 'int',
        'hp' : 'int',
	}

class PlanetSpawn(legume.messages.BaseMessage):
    MessageTypeID = MSGID+2
    MessageValues = {
        'id' : 'int',
        'radius' : 'int',
        'x' : 'int',
        'y' : 'int',
    }

class ShipUpdate(legume.messages.BaseMessage):
    MessageTypeID = MSGID+3
    MessageValues = {
        'id' : 'int',
        'player_color' : 'int',
        'name' : 'string 32'
	}

class ShipUpdateFull(legume.messages.BaseMessage):
    MessageTypeID = MSGID+4
    MessageValues = {
        'id' : 'int',
        'player_color' : 'int',
        'name' : 'string 32'
    }

class ShipSpawn(legume.messages.BaseMessage):
    MessageTypeID = MSGID+5
    MessageValues = {
    	'id' : 'int',
        'parts' : 'varstring',
        'name': 'string 32',

	}

class FloaterUpdate(legume.messages.BaseMessage):
    MessageTypeID = MSGID+6
    MessageValues = {
        'id':'int',
        'x':'int',
        'y':'int',
        'dx':'int',
        'dy':'int'
    }

class FloaterUpdateFull(legume.messages.BaseMessage):
    MessageTypeID = MSGID+7
    MessageValues = {
        'id':'int',
        'x':'int',
        'y':'int'
    }

class FloaterSpawn(legume.messages.BaseMessage):
    MessageTypeID = MSGID+8
    MessageValues = {
        'id':'int',
        'x':'int',
        'y':'int'
    }

class FloaterKill(legume.messages.BaseMessage):
    MessageTypeID = MSGID+9
    MessageValues = {
        'id':'int'
    }

class PartUpdate(legume.messages.BaseMessage):
    MessageTypeID = MSGID+10
    MessageValues = {
        'id' : 'int',
    }

class PartUpdateFull(legume.messages.BaseMessage):
    MessageTypeID = MSGID+11
    MessageValues = {
        'id' : 'int',
    }

class PartSpawn(legume.messages.BaseMessage):
    MessageTypeID = MSGID+12
    MessageValues = {
        'id' : 'int',
    }

class VersionReport(legume.messages.BaseMessage):
    MessageTypeID = MSGID+13
    MessageValues = {
        'id' : 'int',
    }


class SystemUpdate(legume.messages.BaseMessage):
    MessageTypeID = MSGID+14
    MessageValues = {
        'id' : 'int',
	}

class SystemSpawn(legume.messages.BaseMessage):
    MessageTypeID = MSGID+15
    MessageValues = {
        'frame_number' : 'int',
    }

class PlayerMessage(legume.messages.BaseMessage):
    MessageTypeID = MSGID+16
    MessageValues = {
        'frame_number' : 'int',
    }




legume.messages.message_factory.add(PlanetUpdate)
legume.messages.message_factory.add(PlanetSpawn)
legume.messages.message_factory.add(ShipUpdate)
legume.messages.message_factory.add(ShipUpdateFull)
legume.messages.message_factory.add(ShipSpawn)
legume.messages.message_factory.add(FloaterUpdate)
legume.messages.message_factory.add(FloaterUpdateFull)
legume.messages.message_factory.add(FloaterSpawn)
legume.messages.message_factory.add(FloaterKill)
legume.messages.message_factory.add(PartUpdate)
legume.messages.message_factory.add(PartUpdateFull)
legume.messages.message_factory.add(PartSpawn)
legume.messages.message_factory.add(VersionReport)
legume.messages.message_factory.add(SystemUpdate)
legume.messages.message_factory.add(SystemSpawn)
legume.messages.message_factory.add(PlayerMessage)