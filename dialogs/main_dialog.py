import pandas as pd
import userData
import requests

from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions, ChoicePrompt, ConfirmPrompt
from botbuilder.core import MessageFactory, TurnContext, CardFactory, UserState
from botbuilder.schema import InputHints, CardAction, ActionTypes, SuggestedActions
from botbuilder.dialogs.choices import Choice
from .operations.createorder_dialog import CreateOrderDialog
from .operations.vieworder_dialog import ViewOrderDialog
from .operations.cancelorder_dialog import CancelOrderDialog


class MainDialog(ComponentDialog):
    def __init__(
        self, createorder_dialog: CreateOrderDialog, vieworder_dialog: ViewOrderDialog,
        cancelorder_dialog: CancelOrderDialog
    ):
        super(MainDialog, self).__init__(MainDialog.__name__)

        self._createorder_dialog_id = createorder_dialog.id
        self._vieworder_dialog_id = vieworder_dialog.id
        self._cancelorder_dialog_id = cancelorder_dialog.id
        self.add_dialog(createorder_dialog)
        self.add_dialog(vieworder_dialog)
        self.add_dialog(cancelorder_dialog)
        
        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                "WFDialog", [self.userexists_step, self.role_step, self.azexp_step, self.saveuser_step, self.search_step, self.final_step]
            )
        )
        self.initial_dialog_id = "WFDialog"

    async def userexists_step(self, step_context: WaterfallStepContext)-> DialogTurnResult:

        user_details = step_context.options
        email_id = None

        if user_details:
            if user_details.email_id == None:
                email_id = None
            else:
                email_id = user_details.email_id
        else:
            email_id = None
        
        if email_id == None:
            ''' reply = MessageFactory.suggested_actions(
                [CardAction(title = 'Existing USer', type=ActionTypes.im_back, value='Existing User'),
                CardAction(title='New User', type=ActionTypes.im_back, value='Existing User')],  'Existing or new user?')

            return await step_context.prompt(
                ChoicePrompt.__name__,
                PromptOptions(prompt=reply, choices=[Choice('Existing User'), Choice('New User')],
                ),
            ) '''

            message_text = "Welcome to BotBee !!! Please provide your email ID to get started."
            prompt_message =MessageFactory.text(
                    message_text, message_text, InputHints.expecting_input
                )
            return await step_context.prompt(
                    TextPrompt.__name__, PromptOptions(prompt=prompt_message)
                )
        else:
            return await step_context.next(user_details)

    ''' async def emailid_step(self, step_context: WaterfallStepContext)-> DialogTurnResult:
        user_details = step_context.options
        email_id = None

        if user_details:
            if user_details.email_id == None:
                email_id = None
            else:
                email_id = user_details.email_id
        else:
            email_id =None

        if email_id == None:
            step_context.values['UserType'] = step_context.result
            email_id = step_context.values['UserType']
            print(email_id)
            if email_id == "Existing User":
                message_text = "Please enter your user id."
                prompt_message =MessageFactory.text(
                    message_text, message_text, InputHints.expecting_input
                )
                return await step_context.prompt(
                    TextPrompt.__name__, PromptOptions(prompt=prompt_message)
                )
            else:
                N= 7
                email_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k = N))
                user_details.email_id = email_id

                msg_text = "Please note your user id " + email_id
                msg = MessageFactory.text(
                    msg_text, msg_text, InputHints.ignoring_input
                )
                await step_context.context.send_activity(msg)
                return await step_context.next(user_details)
        else:
            return await step_context.next(user_details)
    '''

    async def role_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        user_details = step_context.options
        email_id = None
        
        if user_details:
            if user_details.email_id == None:
                email_id = None
            else:
                email_id = user_details.email_id
        else:
            email_id = None

        if email_id == None:
            if (step_context.result):
                    step_context.values['email_id']= step_context.result
                    user_details.email_id = step_context.values['email_id']
                    #TODO : validate email ID
                    df = userData.getUser(user_details.email_id)
                    if df.size > 0 :
                        step_context.values['role']= df.iloc[0]["role"]
                        user_details.role = step_context.values['role']
                        step_context.values['experience']= df.iloc[0]["experience"]
                        user_details.experience = step_context.values['experience']
                        step_context.values['level']= df.iloc[0]["level"]
                        user_details.level = step_context.values['level']
                        step_context.values['isExistingUser']= True
                        user_details.isExistingUser = step_context.values['isExistingUser']
        
        if user_details.email_id != None and user_details.role == None:
            reply = MessageFactory.suggested_actions(
                [CardAction(title='Administrator', type=ActionTypes.im_back, value='Administrator'),
                CardAction(title='Developer', type=ActionTypes.im_back, value='Developer'),
                CardAction(title='AI Engineer', type=ActionTypes.im_back, value='AI Engineer'),
                CardAction(title='Other', type=ActionTypes.im_back, value='Other'),
                ], 'What is your current role?')

            return await step_context.prompt(
                ChoicePrompt.__name__,
                PromptOptions(
                    prompt=reply,
                    choices=[Choice("Administrator"),Choice("Developer"), Choice("AI Engineer"), Choice("Other")],
                ),
            )
        else:
            return await step_context.next(user_details)

    async def azexp_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        user_details = step_context.options
        role = None
        
        if user_details:
            if user_details.role == None:
                role = None
            else:
                role = user_details.role
        else:
            role = None

        if role == None:
            if (step_context.result):
                step_context.values['role']= step_context.result.value
                user_details.role = step_context.values['role']
                print(user_details.role)

        if user_details.email_id != None and user_details.role != None and user_details.experience == None:
            reply = MessageFactory.suggested_actions(
                [CardAction(title='0-6 months', type=ActionTypes.im_back, value='0-6 months'),
                CardAction(title='6-12 months', type=ActionTypes.im_back, value='6-12 months'),
                CardAction(title='1-2 years', type=ActionTypes.im_back, value='1-2 years'),
                CardAction(title='2+ years', type=ActionTypes.im_back, value='2+ years'),
                ], 'How long you are working on Azure platform?')

            return await step_context.prompt(
                ChoicePrompt.__name__,
                PromptOptions(
                    prompt=reply,
                    choices=[Choice("0-6 months"),Choice("6-12 months"), Choice("1-2 years"), Choice("2+ years")],
                ),
            )
        else:
            return await step_context.next(user_details)

    ''' async def act_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        step_context.values['Operation'] = step_context.result.value
        operation = step_context.values['Operation']

        msg_text = "you have selected " + operation
        msg = MessageFactory.text(
            msg_text, msg_text, InputHints.ignoring_input
        ) 
        await step_context.context.send_activity(msg) 

        user_details = step_context.options
        if operation == "Create Order":
            return await step_context.begin_dialog(self._createorder_dialog_id, user_details)  

        if operation == "View Order":
            return await step_context.begin_dialog(self._vieworder_dialog_id, user_details)

        if operation == "Cancel Order":
            return await step_context.begin_dialog(self._cancelorder_dialog_id, user_details) '''



    async def saveuser_step(self, step_context: WaterfallStepContext)-> DialogTurnResult:
        user_details = step_context.options
        experience = None
        
        if user_details:
            if user_details.experience == None:
                experience = None
            else:
                experience = user_details.experience
        else:
            experience = None

        if experience == None:
            if (step_context.result):
                step_context.values['experience']= step_context.result.value
                user_details.experience = step_context.values['experience']

        if user_details.experience ==  "0-6 months":
            step_context.values['level']= "fundamentals"
            user_details.level = step_context.values['level']
        elif user_details.experience ==  "6-12 months":
            step_context.values['level']= "associate"
            user_details.level = step_context.values['level']
        elif user_details.experience ==  "1-2 years":
            step_context.values['level']= "expert"
            user_details.level = step_context.values['level']
        else:
            step_context.values['level']= "specialty"
            user_details.level = step_context.values['level']
        
        if not user_details.isSaved:
            if user_details.email_id != None and user_details.role != None and user_details.experience != None:
                userData.addUser(user_details)
            
            step_context.values['isSaved'] = True
            user_details.isSaved = step_context.values['isSaved']
            
            if user_details.isExistingUser:
                message_text = "Welcome back to BotBee !!! Please continue with your search..."
            else:
                message_text = "Your registration is completed now with BotBee !!! Please continue with your search..."
            
            message =MessageFactory.text(
                message_text, message_text, InputHints.ignoring_input
            )
            await step_context.context.send_activity(message) 
        return await step_context.next(user_details)

        '''     #return await step_context.end_dialog()
        print(user_details.email_id)
        return await step_context.replace_dialog(self.id, user_details) '''

    async def search_step(self, step_context: WaterfallStepContext)-> DialogTurnResult:
        user_details = step_context.options
        message_text = ""
        prompt_message =MessageFactory.text(
            message_text, message_text, InputHints.expecting_input
        )
        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=prompt_message)
        )
    
    async def final_step(self, step_context: WaterfallStepContext)-> DialogTurnResult:
        user_details = step_context.options

        if (step_context.result):
            message_text = userData._query_language(question=step_context.result, level=user_details.level)
            prompt_message =MessageFactory.text(
                message_text, message_text, InputHints.expecting_input
            )
            await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        #return await step_context.end_dialog()
        return await step_context.replace_dialog(self.id, user_details) 

    def _validate_email_id(self, user_input: str) -> bool:
        regex = '^[a-z0-9]+[\._]?[a-z0-9]*[@]\w+[.]\w{2,3}$' 
        if not (re.search(regex,user_input)):
            return False
        return True

