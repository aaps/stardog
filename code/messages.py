import legume


MSGID = legume.messages.BASE_MESSAGETYPEID_USER
PORT = 6666



class EntityUpdate(legume.messages.BaseMessage):
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

class EntityCreate(legume.messages.BaseMessage):
    MessageTypeID = MSGID+2
    MessageValues = {
        'player_id' : 'int',
        'player_color' : 'int',
        'name' : 'string 32'
	}

class SystemCreate(legume.messages.BaseMessage):
    MessageTypeID = MSGID+3
    MessageValues = {
    	'system_id' : 'int',
    	'name' : 'string 32',
	}

class SystemUpdate(legume.messages.BaseMessage):
    MessageTypeID = MSGID+4
    MessageValues = {
        'frame_number' : 'int',
	}






legume.messages.message_factory.add(EntityUpdate)
legume.messages.message_factory.add(EntityCreate)
legume.messages.message_factory.add(SystemCreate)
legume.messages.message_factory.add(SystemUpdate)