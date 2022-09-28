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

import string
import random

class MainDialog(ComponentDialog):
    def __init__(
        self
    ):
        super(MainDialog, self).__init__(MainDialog.__name__)

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                "WFDialog", [self.userexists_step, self.userid_step, self.intro_step, self.final_step]
            )
        )

        self.initial_dialog_id = "WFDialog"

    async def userexists_step(self, step_context: WaterfallStepContext)-> DialogTurnResult:

        user_details = step_context.options

        user_id = None

        if user_details:
            if user_details.user_id == None:
                user_id = None
            else:
                user_id = user_details.user_id
        else:
            user_id = None
        
        if user_id == None:
            reply = MessageFactory.suggested_actions(
                [CardAction(title = 'Existing User', type=ActionTypes.im_back, value='Existing User'),
                CardAction(title='New User', type=ActionTypes.im_back, value='New User')],  'Existing or new user?')

            return await step_context.prompt(
                ChoicePrompt.__name__,
                PromptOptions(prompt=reply, choices=[Choice('Existing User'), Choice('New User')],
                ),
            )

        else:
            return await step_context.next(user_details)

    async def userid_step(self, step_context: WaterfallStepContext)-> DialogTurnResult:
        user_details = step_context.options
        user_id = None

        if user_details:
            if user_details.user_id == None:
                user_id = None
            else:
                user_id = user_details.user_id
        else:
            user_id =None

        if user_id == None:
            step_context.values['UserType'] = step_context.result.value
            user_type = step_context.values['UserType']

            if user_type == "Existing User":
                message_text = "Please enter your user id."
                prompt_message =MessageFactory.text(
                    message_text, message_text, InputHints.expecting_input
                )
                return await step_context.prompt(
                    TextPrompt.__name__, PromptOptions(prompt=prompt_message)
                )
            else:
                N= 7
                user_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k = N))
                user_details.user_id = user_id

                msg_text = "Please note your user id " + user_id
                msg = MessageFactory.text(
                    msg_text, msg_text, InputHints.ignoring_input
                )
                await step_context.context.send_activity(msg)
                return await step_context.next(user_details)
        else:
            return await step_context.next(user_details)

    async def intro_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        user_details = step_context.options
        user_id = None
        
        if user_details:
            if user_details.user_id == None:
                user_id = None
            else:
                user_id = user_details.user_id
        else:
            user_id = None

        if user_id == None:
            if (step_context.result):
                step_context.values['user_id']= step_context.result
                user_details.user_id = step_context.result

        message_text = "Please provide your order description."
        prompt_message = MessageFactory.text(
            message_text, message_text, InputHints.expecting_input
        )
        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=prompt_message)
        )

        

    async def final_step(self, step_context: WaterfallStepContext)-> DialogTurnResult:
        user_details = step_context.options