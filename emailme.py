import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def emailme(body,filen):
    remitente = 'articusb2022@gmail.com'
    destinatarios = ['aacosta24@unisimonbolivar.edu.co ', 'juvenal.yosa@unisimonbolivar.edu.co']
    asunto = 'Artic USB data analysis'
    cuerpo = body
    ruta_adjunto = filen
    nombre_adjunto = filen
    mensaje = MIMEMultipart()
    mensaje['From'] = remitente
    mensaje['To'] = ", ".join(destinatarios)
    mensaje['Subject'] = asunto
    mensaje.attach(MIMEText(cuerpo, 'plain'))
    archivo_adjunto = open(ruta_adjunto, 'rb')
    adjunto_MIME = MIMEBase('application', 'octet-stream')
    adjunto_MIME.set_payload((archivo_adjunto).read())
    encoders.encode_base64(adjunto_MIME)
    adjunto_MIME.add_header('Content-Disposition', "attachment; filename= %s" % nombre_adjunto)
    mensaje.attach(adjunto_MIME)
    sesion_smtp = smtplib.SMTP('smtp.gmail.com', 587)
    sesion_smtp.starttls()
    sesion_smtp.login('articusb2022@gmail.com','B10s1l1c0!')
    texto = mensaje.as_string()
    sesion_smtp.sendmail(remitente, destinatarios, texto)
    sesion_smtp.quit()