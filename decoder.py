import datetime
import base64

# hexadecimal string
# Example String hex = '29052001782A00EF0338FFFF' 

def decode(base64_str):
   
    decodedBytes = base64.b64decode(base64_str)
    hex = decodedBytes.hex()
    payload ={
        'id' : str(hex[0:8]),
        'battery_voltage' : int(hex[8:10],16)*30,
        'rssi' : int(hex[10:12],16),
        'temperature' : int(hex[12:16],16)/10,
        'humidity' : int(hex[16:20],16),
        'resistance' : int(hex[20:24],16)/10
    #    'alarms' : int(hex[24:25],16)    
    }
    return payload
    
def create_c8y_payload(fragment,series,value,internal_id):
        payload = {}
        payload['source'] = {"id": str(internal_id)}
        payload['type'] = "NBIoTType"
        payload['time'] = datetime.datetime.strptime(str(datetime.datetime.utcnow()), '%Y-%m-%d %H:%M:%S.%f').isoformat() + "Z"
        frag = {}
        frag[str(series)] = {'value': value}
        payload[str(fragment)] = frag
        return payload

