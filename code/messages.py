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
        'entity_id' : 'int',
        'frame_number' : 'int',
        'name' : 'string 32',
        'x' : 'int',
        'y' : 'int',
        'dx' : 'int',
        'dy' : 'int',
        'hp' : 'int',
    }

class ShipUpdate(legume.messages.BaseMessage):
    MessageTypeID = MSGID+3
    MessageValues = {
        'player_id' : 'int',
        'player_color' : 'int',
        'name' : 'string 32'
	}

class ShipSpawn(legume.messages.BaseMessage):
    MessageTypeID = MSGID+4
    MessageValues = {
    	'system_id' : 'int',
    	'name' : 'string 32',
	}

class FloaterUpdate(legume.messages.BaseMessage):
    MessageTypeID = MSGID+5
    MessageValues = {
        'frame_number' : 'int',
    }

class FloaterSpawn(legume.messages.BaseMessage):
    MessageTypeID = MSGID+6
    MessageValues = {
        'frame_number' : 'int',
    }

class PartUpdate(legume.messages.BaseMessage):
    MessageTypeID = MSGID+7
    MessageValues = {
        'frame_number' : 'int',
    }

class PartSpawn(legume.messages.BaseMessage):
    MessageTypeID = MSGID+8
    MessageValues = {
        'frame_number' : 'int',
    }


class SystemUpdate(legume.messages.BaseMessage):
    MessageTypeID = MSGID+9
    MessageValues = {
        'frame_number' : 'int',
	}

class SystemSpawn(legume.messages.BaseMessage):
    MessageTypeID = MSGID+10
    MessageValues = {
        'frame_number' : 'int',
    }

class PlayerMessage(legume.messages.BaseMessage):
    MessageTypeID = MSGID+11
    MessageValues = {
        'frame_number' : 'int',
    }




legume.messages.message_factory.add(PlanetUpdate)
legume.messages.message_factory.add(PlanetSpawn)
legume.messages.message_factory.add(ShipUpdate)
legume.messages.message_factory.add(ShipSpawn)
legume.messages.message_factory.add(FloaterUpdate)
legume.messages.message_factory.add(FloaterSpawn)
legume.messages.message_factory.add(PartUpdate)
legume.messages.message_factory.add(PartSpawn)
legume.messages.message_factory.add(SystemUpdate)
legume.messages.message_factory.add(SystemSpawn)
legume.messages.message_factory.add(PlayerMessage)