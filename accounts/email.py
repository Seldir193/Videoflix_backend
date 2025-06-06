from djoser.email import ActivationEmail, PasswordResetEmail

class CustomActivationEmail(ActivationEmail):
    template_name       = "djoser/email/activation.html"   
    plain_template_name = "djoser/email/activation.txt"
    subject             = "Aktiviere dein Konto bei Videoflix"

class CustomPasswordResetEmail(PasswordResetEmail):
    template_name       = "djoser/email/password_reset.html"
    plain_template_name = "djoser/email/password_reset.txt"
    subject             = "Setze dein Videoflix-Passwort zurück"
