###############################
## AGENTE DESARROLADO POR JJ ##
###############################

#Version de python: 3.11.9

########################
## CONFIGURACION SMTP ##
########################

#Descargar libreria PYSNMP
#pip uninstall pysnmp -y
#pip install pysnmp==4.4.12
#Descargar libreria PYASN1
#pip uninstall pyasn1 -y
#pip install pyasn1==0.4.8

#Liberias necesarias
import smtplib
from pysnmp.hlapi import (
    SnmpEngine, CommunityData, UdpTransportTarget,
    ContextData, ObjectType, ObjectIdentity, getCmd
)
import importlib

# Configuracion SNMP
target_ip = "10.234.66.22"
community = "public"  # Cambia esto si usas una comunidad diferente
# oid = '1.3.6.1.2.1.1.5.0' # OID para modelo
oid = '1.3.6.1.4.1.12612.220.11.2.2.10.5.1.2.1'  # OID para alerta activa

# Consulta SNMP
def snmp_get(ip, community, oid):
    error_indication, error_status, error_index, var_binds = next(
        getCmd(SnmpEngine(),
               CommunityData(community, mpModel=0),  # SNMPv1
               UdpTransportTarget((ip, 161)),
               ContextData(),
               ObjectType(ObjectIdentity(oid)))
    )

    if error_indication:
        return f"SNMP error: {error_indication}"
    elif error_status:
        return f"{error_status.prettyPrint()}"
    else:
        for varBind in var_binds:
            return f'{varBind[1]}'

# Obtener info SNMP
device_name = snmp_get(target_ip, community, oid)

#################################################
## ENVIO DE CORREO ELECTRONICO POR OUTLOOK 365 ##
#################################################

import smtplib
from email.message import EmailMessage

# Configuración Outlook
email = "odooav@cineplanet.com.pe"
password = "PlexPEOA25%"
receiver_email = "jpardo@cineplanet.com.pe"
smtp_server = "smtp.office365.com"
port = 587

# Datos del mensaje
subject = target_ip  # Asume que estas variables están definidas
message = device_name

# Crear mensaje con formato adecuado
msg = EmailMessage()
msg['From'] = email
msg['To'] = receiver_email
msg['Subject'] = subject
msg.set_content(message)

try:
    # Conexión segura
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()  # Habilita TLS
        server.login(email, password)
        server.send_message(msg)
        print(f"Email enviado exitosamente a {receiver_email}")
        
except Exception as e:
    print(f"Error al enviar el correo: {str(e)}")

###################################
## ENVIO DE MENSAJE POR WHATSAPP ##
###################################

import requests

url = "https://graph.facebook.com/v22.0/745562308629793/messages"
headers = {
    "Authorization": "Bearer EAAKPKAtBUfcBO77djZArMNxMAsUR63D3CVpRVpaMNdOfZCumYzvcBj1zdl2TXXQQZA7CJdXT0RZC6ZBwalrhN6aDHjZAziLAs8yS62JTy5lRKCv2s1bIFZBeJiZBnPXsyEZCzeYenMJhCI0EQRRqW4XDKwQK4I5DCwiebGEWSSO1NW9b98rGoG5G3aoXVhZAdlflOmpdZAO2MZBGamiEhwdB4oz9zEUYw1GFgmEXDwEZD",
    "Content-Type": "application/json"
}
data = {
    "messaging_product": "whatsapp",
    "to": "51981283879",
    "type": "text",
    "text": {"body": "Mensaje automático desde API"}
}

try:
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    
    if response.status_code == 200:
        print("✅ Mensaje enviado. ID:", result["messages"][0]["id"])
    else:
        print("❌ Error:", result.get("error", {}).get("message", "Desconocido"))
        
except Exception as e:
    print("⚠️ Error en la conexión:", str(e))

# Finalización del script