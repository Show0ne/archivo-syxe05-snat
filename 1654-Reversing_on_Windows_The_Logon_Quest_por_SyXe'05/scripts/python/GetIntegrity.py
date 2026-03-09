
import struct
from ctypes import *
import sys

class OBJECT_ATTRIBUTES(Structure):
	_fields_ = [
	    ("Length", c_char_p),
		("RootDirectory", c_char_p),
		("ObjectName", c_char_p),
		("Attributes", c_char_p),
		("SecurityDescriptor", c_char_p),
		("SecurityQualityOfService", c_char_p)]

class GetIntegrity:

	def getIntegrityLevel( self, filename ):
		# valores validos
		integrities = (0x0, 0x1000, 0x2000, 0x3000, 0x4000)

		# definimos un alias para las librerias
		advapi = windll.advapi32
		kernel = windll.kernel32
		msvcrt = cdll.msvcrt
		ntdll = windll.ntdll

		# Creamos la estructura OBJECT_ATTRIBUTES
		nt_struct = OBJECT_ATTRIBUTES()
		nt_struct.Length = struct.pack('<i4', 0x18)
		nt_struct.RootDirectory = struct.pack('<i4', 0)
		nt_struct.ObjectName = struct.pack('<i4', 0)
		nt_struct.Attributes = struct.pack('<i4', 0x40)
		nt_struct.SecurityDescriptor = struct.pack('<i4', 0)
		nt_struct.SecurityQualityOfService = struct.pack('<i4', 0)

		# no attributtes error, continuamos, hay que 'relativizar' el path al archivo
		pRelativeName =  create_string_buffer(0x40)
		UNICODE_STRING =  create_string_buffer(0x8)
		status_code = ntdll.RtlDosPathNameToRelativeNtPathName_U(
			filename, byref(UNICODE_STRING), 0x0, byref(pRelativeName)
		)
		# si va todo bien retorna EAX==0x1(ALL_OK)

		# salvamos la direccion de la cadena en nuestra estructura
		nt_struct.ObjectName = struct.pack('<i4', addressof(UNICODE_STRING))

		# Y la pasamos a un buffer
		nt_buffer = create_string_buffer(sizeof(nt_struct))
		msvcrt.memcpy(
			byref(nt_buffer, 0),
			nt_struct.Length,
			1
		)
		msvcrt.memcpy(
			byref(nt_buffer, 4),
			nt_struct.RootDirectory,
			len(nt_struct.RootDirectory)
		)
		msvcrt.memcpy(
			byref(nt_buffer, 8),
			nt_struct.ObjectName,
			4
		)
		msvcrt.memcpy(
			byref(nt_buffer, 0xC),
			nt_struct.Attributes,
			1
		)
		msvcrt.memcpy(
			byref(nt_buffer, 0x10),
			nt_struct.SecurityDescriptor,
			len(nt_struct.SecurityDescriptor)
		)
		msvcrt.memcpy(
			byref(nt_buffer, 0x14),
			nt_struct.SecurityQualityOfService,
			len(nt_struct.SecurityQualityOfService)
		)

		# Y seguimos por ntdll.NtOpenFile
		ret_handle = create_string_buffer(0x4)
		pStatusBlock = create_string_buffer(0x8)
		status_code = ntdll.NtOpenFile(
			byref(ret_handle),
			0x20080,
			byref(nt_buffer),
			byref(pStatusBlock),
			0x7,
			0x200000
		)
		# retorna EAX==0x0(ALL_OK) sio todo fue bien

		# dereferenciamos el handle
		puntero = cast(ret_handle, POINTER(c_int))
		handle = c_int(puntero[0])

		# Si el manejador es 0x0 hubo algun problema, abortamos
		if (handle.value == 0x0):
			print " Error: no es posible abrir %s"%filename
			return

		# Seguimos por GetSecurityInfo
		pSecurityInfo = create_string_buffer(0x100)
		status_code = windll.advapi32.GetSecurityInfo(
			handle, 0x1,
			0x17,
			0x0,
			0x0,
			0x0,
			0x0,
			byref(pSecurityInfo)
		)
		# si la llamada tiene exito retorna EAX==0x0(ALL_OK)

		# Cerramos el manejador de archivo
		close_status = windll.kernel32.CloseHandle(handle)
		descriptor_pointer = addressof(pSecurityInfo)
		descriptor_addr = c_int(cast(descriptor_pointer, POINTER(c_int))[0])

		#Y leemos el nivel de integridad
		offset_sacl_addr = descriptor_addr.value + 0xC
		offset_sacl_value = c_int(cast(offset_sacl_addr, POINTER(c_int))[0])


		# Mira si el puntero esta a 0x0 y si es asi informa y aborta
		if (offset_sacl_value.value == 0x0):
			print " Sin informacion de Integridad"
			return

		starting_sacl = descriptor_addr.value + offset_sacl_value.value
		sacl_len_offset = c_int(starting_sacl + 0x2)
		sacl_len_value = c_int(
			cast(sacl_len_offset.value, POINTER(c_byte))[0]
		)


		integrity_address = starting_sacl + sacl_len_value.value - 0x4
		integrity_value = c_int(cast(integrity_address, POINTER(c_int))[0])

		if not integrity_value.value in integrities:
			print " Sid no encontrada", hex(integrity_value.value)
		else:
			sid = 'S-1-16-' + hex(integrity_value.value)
			print "   Sid:", sid
			if integrity_value.value == integrities[0]:
				print " Level: UNTRUSTED"
			if integrity_value.value == integrities[1]:
				print " Level: LOW"
			if integrity_value.value == integrities[2]:
				print " Level: MEDIUM"
			if integrity_value.value == integrities[3]:
				print " Level: HIGH"
			if integrity_value.value == integrities[4]:
				print " Level: SYSTEM"

def showUsage():
    sys.__stderr__.write(
    """ uso: %s archivo
     -archivo: ruta absoluta al archivo de trabajo.

     @Ejemplo: python %s c:\miArchivo.txt
               python %s c:\\ejecutame.exe
                        """%(sys.argv[0],sys.argv[0],sys.argv[0]))

def printheader():
    print "\n IntegrityX v1.0 - Utilidad para obtener el Nivel de Integridad"
    print " The Fast Lane (c) 2018 - SyXe'05[cls]"
    print " syxe05@gmail.com\n"

if __name__ == '__main__':
	printheader()
	a = sys.argv[1:]
	if (a.__len__() != 1):
		showUsage()
		sys.exit(1)

	filename = create_unicode_buffer(a[0])
	integrity = GetIntegrity()
	integrity.getIntegrityLevel(filename)