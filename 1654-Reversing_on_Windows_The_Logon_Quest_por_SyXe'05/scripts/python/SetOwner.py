
import struct
from ctypes import *
import sys
from EnableAllPrivs import *

__all__ = ["SetOwner"]

class TOKEN_PRIVILEGE(Structure):
	_fields_ = [
	    ("privilegeCount", c_char_p),
		("privilege_luid", c_char_p),
		("zeros", c_char_p),
		("SE_PRIVILEGE_ENABLED", c_char_p)]

class OBJECT_ATTRIBUTES(Structure):
	_fields_ = [
	    ("Length", c_char_p),
		("RootDirectory", c_char_p),
		("ObjectName", c_char_p),
		("Attributes", c_char_p),
		("SecurityDescriptor", c_char_p),
		("SecurityQualityOfService", c_char_p)]

class SetOwner:
	
	def setOwner( self, filename, owner ):
		phToken = c_void_p()
		pSid =  create_string_buffer(0x64)
		pLen =  create_string_buffer(0x64)
		pMachine =  create_string_buffer(0x64)
		pCeroCinco =  create_string_buffer(0x64)
		pRet =  create_string_buffer(0x64)

		#<user_name> = c_wchar_p(owner)
		admin_name = c_wchar_p(owner)

		# obtenemos el tamanyo de bufer primero
		get_account = windll.advapi32.LookupAccountNameW(
				0x0,
				admin_name,
				byref(pSid),byref(pLen),
				byref(pMachine),
				byref(pCeroCinco),
				byref(pRet)
		)

		# Hacemos la llamada
		get_account = windll.advapi32.LookupAccountNameW(
				0x0,
				admin_name,
				byref(pSid),
				byref(pLen),
				byref(pMachine),
				byref(pCeroCinco),
				byref(pRet)
		)

		pid = windll.kernel32.GetCurrentProcessId()
		handle_process = windll.kernel32.OpenProcess(0x400, 0, pid)

		# Dejamos el handle de nuestro token en POINTER(phToken)
		phToken = c_void_p()
		handle_token_status = windll.kernel32.OpenProcessToken(
			handle_process,
			0x28,
			byref(phToken)
		)

		tk = TOKEN_PRIVILEGE()
		tk.privilegeCount = struct.pack('<i4', 1)
		tk.privilege_luid = struct.pack('<i4', 0)
		tk.zeros = struct.pack('<i4', 0)
		tk.SE_PRIVILEGE_ENABLED = struct.pack('<i4', 2)

		# Habilitamos el privilegio "SeRestorePrivilege" en nuestro
		# access token lo que causara que NTFS nos permita el acceso
		# a cualquier archivo o directorio, en particular para las
		# siguientes operaciones:
		#
		#    WRITE_DAC
		#    WRITE_OWNER  // Esta es la que queremos :)
		#    ACCESS_SYSTEM_SECURITY
		#    FILE_GENERIC_WRITE
		#    FILE_ADD_FILE
		#    FILE_ADD_SUBDIRECTORY
		#
		#e_priv = EnablePriv()
		e_priv = EnableAllPrivs()
		e_priv.enable()



		# Y habilitamos el privilegio "SeTakeOwnershipPrivilege" que nos permitira
		# obtener la propiedad de un objeto aun cuando no se nos conceda el acceso
		# 'discretionary'
		#
		access_mask = create_string_buffer(0x8)
		set_access_mask = windll.advapi32.SetSecurityAccessMask(
			0x1, byref(access_mask)
		)


		#
		# Copiamos los valores
		#
		nt_struct = OBJECT_ATTRIBUTES()
		nt_struct.Length = struct.pack('<i4', 0x18)
		nt_struct.RootDirectory = struct.pack('<i4', 0x0)
		nt_struct.ObjectName = struct.pack('<i4', 0x0)
		nt_struct.Attributes = struct.pack('<i4', 0x40)
		nt_struct.SecurityDescriptor = struct.pack('<i4', 0x0)
		nt_struct.SecurityQualityOfService = struct.pack('<i4', 0x0)

		pRelativeName =  create_string_buffer(0x40)
		UNICODE_STRING =  create_string_buffer(0x8)
		rtldpn_status = windll.ntdll.RtlDosPathNameToRelativeNtPathName_U(
			filename,
			byref(UNICODE_STRING),
			0x0,
			byref(pRelativeName)
		)

		nt_struct.ObjectName = struct.pack('<i4', addressof(UNICODE_STRING))
		ret_handle = create_string_buffer(0x4)
		nt_buffer = create_string_buffer(sizeof(nt_struct))

		copied =cdll.msvcrt.memcpy(
			byref(nt_buffer, 0), nt_struct.Length, 1 )
		copied =cdll.msvcrt.memcpy(
			byref(nt_buffer, 4),
			nt_struct.RootDirectory,
			len(nt_struct.RootDirectory)
		)
		copied =cdll.msvcrt.memcpy(
			byref(nt_buffer, 8), nt_struct.ObjectName, 4 )
		copied =cdll.msvcrt.memcpy(
			byref(nt_buffer, 0xC), nt_struct.Attributes, 1 )
		copied =cdll.msvcrt.memcpy(
			byref(nt_buffer, 0x10),
			nt_struct.SecurityDescriptor,
			len(nt_struct.SecurityDescriptor)
		)
		copied =cdll.msvcrt.memcpy(
			byref(nt_buffer, 0x14),
			nt_struct.SecurityQualityOfService,
			len(nt_struct.SecurityQualityOfService)
		)

		pStatusBlock = create_string_buffer(0x8)

		#
		# Calculate MASK!
		#
		# We need the value 0xA0080 for the mask
		#
		FIRST_MASK = 0x04000000
		FIRST_MASK >>= 1
		FIRST_MASK = ~FIRST_MASK
		FIRST_MASK &= 0x80

		mask = cast(access_mask, POINTER(c_int))
		mask = c_int(mask[0])
		mask.value |= 0x20000
		mask.value |= FIRST_MASK

		ntopen_status = windll.ntdll.NtOpenFile(
			byref(ret_handle),
			mask.value,
			byref(nt_buffer),
			byref(pStatusBlock),
			0x7,
			0x200000
		)
		ptr = cast(ret_handle, POINTER(c_int))
		handle = c_int(ptr[0])

		status = windll.advapi32.SetSecurityInfo(
			handle, 0x1, 0x1, byref(pSid), 0x0, 0x0, 0x0
		)
		close_status = windll.kernel32.CloseHandle(handle)

		if (status==0x0):
			print "  owner:",owner
			print " Status: Done!"
		else:
			print " Status: Error!"

def showUsage():
    sys.__stderr__.write(
    """ uso: %s [archivo, owner]
     -archivo: ruta absoluta al archivo de trabajo.
     -owner: nombre del nuevo propietario

     @Ejemplo: python %s c:\\miArchivo.txt Administrador
               python %s c:\\ejecutame.exe SyXe'05
                        """%(sys.argv[0],sys.argv[0],sys.argv[0]))

def printheader():
    print "\n SetOwnerX v1.0 - Utilidad para establecer nuevo propietario"
    print " The Fast Lane (c) 2018 - SyXe'05[cls]"
    print " syxe05@gmail.com\n"

if __name__ == '__main__':
	printheader()
	a = sys.argv[1:]
	if (a.__len__() != 2):
		showUsage()
		sys.exit(1)
	else:
		filename = a[0]
		owner = a[1]
	filename = create_unicode_buffer(a[0])
	s_own = SetOwner()
	s_own.setOwner(filename, owner)