import re

from plone.directives import form
from zope.interface import Interface
from zope.interface import Invalid
from zope import schema
from z3c.form import field, button, validator
from Products.statusmessages.interfaces import IStatusMessage
from tdf.siteaccountrequest import _


from collective.z3cform.norobots.widget import NorobotsFieldWidget
from collective.z3cform.norobots.validator import NorobotsValidator

from plone import api



# Define a validation method for the email address of the user
class NotAnEmailAddress(schema.ValidationError):
    __doc__ = _(u"Invalid email address")

checkEmail = re.compile(
    r"[a-zA-Z0-9._%-]+@([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,4}").match

def validateEmail(value):
    if not checkEmail(value):
        raise Invalid(_(u"Invalid email address"))
    return True



MESSAGE_TEMPLATE = """\

Account Request from %(firstname)s %(name)s <%(emailAddress)s> for LibreOffice Extensions site

Firstname: %(firstname)s
Name: %(name)s
Email: %(emailAddress)s
Preferred Username: %(preferredusername)s



%(message)s
"""





class ISiteAccountForm(Interface):
    """Define the fields of our form
    """

    form.mode(explanation='display')
    explanation=schema.Text(
        title=_(u"Important Information:"),
        description=_(u"You do not need an account to download templates or extensions from this site!"),
        required=False,
        )

    form.mode(requestofaccount='display')
    requestofaccount= schema.Text(
        title =_(u"Account for your Product on the LibreOffice Extension-Template-Test-Site"),
        description=_(u"Submit the form below in case you created a LibreOffice AddOn Product (extension or template) and want to publish it on this site."),
        required=False,
        )
    form.mode(infofirstextensionuploadtiming='display')
    infofirstextensionuploadtiming = schema.Text(
        title =_(u"Please upload your product after you have received the credentials. Projects without files will be deleted after two weeks without further notice!"),
        required=False,
    )


    name = schema.TextLine(
        title=_(u"Lastname"),
        )


    firstname = schema.TextLine(
        title=_(u"Firstname"),
        )

    preferredusername = schema.ASCIILine(
        title=_(u"User Name (5 - 15 ASCII characters)"),
        description=_(u"Please suggest your desired username. In case your preferred username is already taken, we will add numbers to your suggestion."),
        min_length=5,
        max_length=15,
        required=False,
        )



    emailAddress = schema.ASCIILine(
        title=_(u"Your Email Address (required)"),
        constraint=validateEmail
    )


    form.mode(leaveblank='hidden')
    leaveblank = schema.ASCIILine(
        title=_(u'Please leave empty'),
        required=False,
    )


    form.mode(leaveblank='hidden')
    leaveblank = schema.ASCIILine(
        title=_(u'Please leave empty'),
        required=False,
    )


    message = schema.Text(
        title=_(u"Short Description of Your Project or the Reason, why You are asking for an Account"),
        description=_(u"Please keep between 50 to 1,000 characters"),
        min_length=50,
        max_length=1000,
        required=True,

        )

    form.widget(norobots=NorobotsFieldWidget)
    norobots = schema.TextLine(title=_(u'Are you a human ?'),
                               description=_(u'In order to avoid spam, please answer the question below.'),
                               required=True,
                               )


fields = field.Fields(ISiteAccountForm)
fields['norobots'].widgetFactory = NorobotsFieldWidget

validator.WidgetValidatorDiscriminators(NorobotsValidator, field=ISiteAccountForm['norobots'])



class SiteAccountForm(form.SchemaForm):

    schema = ISiteAccountForm

    label = _(u"Hosting your Product(s) (Registration)")
    description = _(u"Please leave a short description of your project below.")

    ignoreContext = True



    # Hide the editable border and tabs
    def update(self):
        self.request.set('disable_border', True)
        return super(SiteAccountForm, self).update()

    @button.buttonAndHandler(_(u"Send"))
    def sendMail(self, action):
        """Send the email to the site administrator and redirect to the
        front page, showing a status message to say the message was received.
        """

        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return


        elif 'leaveblank' in data and data['leaveblank']:

            portal = api.portal.get()

            self.request.response.redirect(portal.absolute_url())
            return

        else:

            portal = api.portal.get()

            # Construct and send a message
            source = "%s" % (data['emailAddress'])
            topic = "%s  %s %s" % ('Asking for an Account on this Site from', data['firstname'], data['name'])
            message = MESSAGE_TEMPLATE % data

            api.portal.send_email(
                recipient = str(source),
                subject = topic,
                body = message
            )


            # Issue a status message
            confirm = _(u"Thank you! Your request for an account has been received and we will create an account. You will get an email with a link to activate your account and reset the password.")
            IStatusMessage(self.request).add(confirm, type='info')

            # Redirect to the portal front page. Return an empty string as the
            # page body - we are redirecting anyway!
            self.request.response.redirect(portal.absolute_url())
            return ''

    @button.buttonAndHandler(_(u"Cancel"))
    def cancelForm(self, action):

        portal = api.portal.get()

        # Redirect to the portal front page. Return an empty string as the
        # page body - we are redirecting anyway!
        self.request.response.redirect(portal.absolute_url())
        return u''



