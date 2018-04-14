import base64


def download_address_translation(original_address):
    original_address = str(original_address)
    if "thunder://" in original_address:
        original_address = original_address.replace('thunder://', '')
        original_address = base64.b64decode(original_address)
        original_address = original_address.decode('gbk')
        original_address = original_address[2:len(original_address) - 2]
    if "flashget://" in original_address:
        original_address = original_address.replace('flashget://', '')
        original_address = original_address.replace('flashget://', '')
        original_address = base64.b64decode(original_address)
        original_address = original_address.decode('gbk')
        original_address = original_address[10:len(original_address) - 10]
    if "qqdl://" in original_address:
        original_address = original_address.replace('qqdl://', '')
        original_address = original_address.replace('qqdl://', '')
        original_address = base64.b64decode(original_address)
        original_address = original_address.decode('gbk')
    temp_address = "AA"
    original_address
    "ZZ"
    temp_address = bytes(temp_address, encoding='gbk')
    thunder_address = "thunder://"
    base64.b64encode(temp_address).decode('gbk')

    temp_address = "[FLASHGET]"
    original_address
    "[FLASHGET]"
    temp_address = bytes(temp_address, encoding='gbk')
    flashget_address = "flashget://"
    base64.b64encode(temp_address).decode('gbk')

    temp_address = original_address
    temp_address = bytes(temp_address, encoding='gbk')
    qqdl_address = "qqdl://"
    base64.b64encode(temp_address).decode('gbk')

    return {'origin': original_address, 'thunder': thunder_address, 'flashget': flashget_address, 'qqdl': qqdl_address}


address = download_address_translation(
    'thunder://QUFlZDJrOi8vfGZpbGV8tcHEubHKvMcuSEQxMjgws6zH5bn60 /W0NOiy6vX1i5tcDR8MzA3NDc3Njk5NXxCOEE2OEY5RDQ2RkZGMzlEQzAzNUYzMEJCRkUzMDA4NHxoPVRXWkJWQkdIMlNRRURCTkFCM0M3WEdZQVRTSDY0RUoyfC9aWg==')
print('原始下载地址:', address.get('origin'))
print('迅雷下载地址:', address.get('thunder'))
print('快车下载地址:', address.get('flashget'))
print('QQ旋风下载地址:', address.get('qqdl'))
