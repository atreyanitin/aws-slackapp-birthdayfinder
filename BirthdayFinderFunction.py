import json
import datetime
import time
import os
import dateutil.parser
import logging
import random



logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# --- Helpers that build all of the responses ---

def load_birthday():
    # Birthday
    birthday = {
    'Mike Langmore' : 'Aug 21st 1986',
    'John Smith' : 'May 23rd 1989',
    'Josh Davis': 'Nov 11th 1972',
    'Sara Goodman': 'Jan 2nd 1984',
    'Sam Bird':'Feb 15th 1992'
    }
    return birthday

    
def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message
        }
    }


def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response


def try_ex(func):
    """
    Call passed in function in try block. If KeyError is encountered return None.
    This function is intended to be used to safely access dictionary.

    Note that this function would have negative impact on performance.
    """

    try:
        return func()
    except KeyError:
        return None


def find_birthday(intent_request):
    """
    Performs dialog management and fulfillment for booking a hotel.

    Beyond fulfillment, the implementation for this intent demonstrates the following:
    1) Use of elicitSlot in slot validation and re-prompting
    2) Use of sessionAttributes to pass information that can be used to guide conversation
    """

    first_name = try_ex(lambda: intent_request['currentIntent']['slots']['FirstName'])
    last_name = try_ex(lambda: intent_request['currentIntent']['slots']['LastName'])
    logger.debug("Entered in find_birthday" )

    session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}

    if intent_request['invocationSource'] == 'FulfillmentCodeHook':
        logger.debug("Entered in FulfillmentCodeHook")
        if first_name and last_name:
            logger.debug("Received both First Name and Last Name")
            session_attributes['FirstName'] = first_name
            session_attributes['LastName'] = last_name
            answer = load_birthday()[first_name+ ' '+ last_name]
            session_attributes['birthday'] = answer
            logger.debug("Received FirstName and LastName. Now Going to find Birthday")
        else:
            try_ex(lambda: session_attributes.pop('FirstName'))


    return close(
        session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': 'Awesome, seems like I found the answer...'+ session_attributes['FirstName'] +' '+ session_attributes['LastName'] +  ' has birthday on '+ session_attributes['birthday']
        }
    )


def dispatch(intent_request):

    intent_name = intent_request['currentIntent']['name']
    logger.debug("Entered in dispatch" + intent_name)
    # Dispatch to your bot's intent handlers
    if intent_name == 'FindBirthday':
        return find_birthday(intent_request)

    raise Exception('Intent with name ' + intent_name + ' not supported')



# --- Main handler ---


def lambda_handler(event, context):
    return dispatch(event)
