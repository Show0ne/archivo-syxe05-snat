
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

class GainAccess:

	def grantFullAccess( self, user, filename ):
		print " Archivo:", filename
		print " Usuario:", user

		if ( not (self.existsFile(filename))):
			print" El archivo no existe o no se puede leer!"
			return

		nt_struct = OBJECT_ATTRIBUTES()
		nt_struct.Length = struct.pack('<i4', 0x18)
		nt_struct.RootDirectory = struct.pack('<i4', 0)
		nt_struct.ObjectName = struct.pack('<i4', 0)
		nt_struct.Attributes = struct.pack('<i4', 0x40)
		nt_struct.SecurityDescriptor = struct.pack('<i4', 0)
		nt_struct.SecurityQualityOfService = struct.pack('<i4', 0)

		phToken = c_void_p()
		pSid =  create_string_buffer(0x64)
		pLen =  create_string_buffer(0x64)
		pMachine =  create_string_buffer(0x64)
		pCeroCinco =  create_string_buffer(0x64)
		pRet =  create_string_buffer(0x64)

		file_name = c_wchar_p(filename)
		admin_name = c_wchar_p(user)

		# Obtenemos el tamanyo del buffer
		get_account = windll.advapi32.LookupAccountNameW(
			0x0,
			admin_name,
			byref(pSid),
			byref(pLen),
			byref(pMachine),
			byref(pCeroCinco),
			byref(pRet)
		)

		# Ahora si obtenemos el valor buscado
		get_account = windll.advapi32.LookupAccountNameW(
			0x0,
			admin_name,
			byref(pSid),
			byref(pLen),
			byref(pMachine),
			byref(pCeroCinco),
			byref(pRet)
		)

		# Sacamos el largo de la SID (no todas tienen el mismo)
		len_sid = windll.advapi32.GetLengthSid(byref(pSid))
		pLenSid =  create_string_buffer(len_sid)
		
		# hay que copiar la SID a un buffer con este layout:
		#
		# 	DWORD DWORD <...SID...>
		#
		# para ello hay que:
		#
		#	1.- ubicar un buffer con valor len(SID) + 0x8
		#	2.- copiar 0x0 en buffer y buffer+0x1
		#	3.- copiar sidMasOcho en buffer+0x2
		#	4.- copiar 0x001F01FF (FULL_ACCESS) en buffer+0x4
		#	5.- copiar la SID real (len==0x1C) en buffer+0x8 (pSid)
		#
		sidMasOcho = c_int()
		sidMasOcho.value = len_sid + 8
		malloc_sidMasOcho = create_string_buffer(sidMasOcho.value)
		cdll.msvcrt.memcpy(byref(malloc_sidMasOcho, 2), pointer(sidMasOcho), 4)
		cdll.msvcrt.memcpy(byref(malloc_sidMasOcho, 4), struct.pack('<i4', 0x001F01FF), 4)
		cdll.msvcrt.memcpy(byref(malloc_sidMasOcho, 8), pSid, len_sid)
		
		file_attrs = windll.kernel32.GetFileAttributesW(file_name)

		pRelativeName =  create_string_buffer(0x40)
		UNICODE_STRING =  create_string_buffer(0x8)
		rtldpn_status = windll.ntdll.RtlDosPathNameToRelativeNtPathName_U(
			file_name,
			byref(UNICODE_STRING),
			0x0,
			byref(pRelativeName)
		)

		nt_struct.ObjectName = struct.pack('<i4', addressof(UNICODE_STRING))

		ret_handle = create_string_buffer(0x4)

		nt_buffer = create_string_buffer(sizeof(nt_struct))

		copied =cdll.msvcrt.memcpy(byref(nt_buffer, 0), nt_struct.Length, 1)
		copied =cdll.msvcrt.memcpy(byref(nt_buffer, 4), nt_struct.RootDirectory, 1)
		copied =cdll.msvcrt.memcpy(byref(nt_buffer, 8), nt_struct.ObjectName, 4)
		copied =cdll.msvcrt.memcpy(byref(nt_buffer, 0xC), nt_struct.Attributes, 1)
		copied =cdll.msvcrt.memcpy(byref(nt_buffer, 0x10), nt_struct.SecurityDescriptor, 1)
		copied =cdll.msvcrt.memcpy(byref(nt_buffer, 0x14), nt_struct.SecurityQualityOfService, 1)

		pStatusBlock = create_string_buffer(0x8)
		ntopen_status = windll.ntdll.NtOpenFile(
			byref(ret_handle),
			0x20080,
			byref(nt_buffer),
			byref(pStatusBlock),
			0x7,
			0x00200000
		)
		ptr = cast(ret_handle, POINTER(c_int))
		handle = c_int(ptr[0])

		# nos vamos a NtQueryInformationFile
		pAuxBuffer = create_string_buffer(0x8)
		zwQuery_status = windll.ntdll.ZwQueryInformationFile(
			handle,
			byref(pAuxBuffer),
			byref(pStatusBlock),
			0x23,
			 0x8
		)

		# nos vamos a GetSecurityInfo
		pSecInfoBuffer = create_string_buffer(0x80)
		getSecurity_status = windll.advapi32.GetSecurityInfo(
			handle,
			0x1,
			0x17,
			0x0,
			0x0,
			0x0,
			0x0,
			byref(pSecInfoBuffer)
		)

		# cerramos el manejador de archivo (handle)
		close_status = windll.kernel32.CloseHandle(handle)

		# vamos a GetSecurityDescriptorDacl
		pb1 = create_string_buffer(0x8)
		pSecDescrDACL = create_string_buffer(0x8)
		pb3 = create_string_buffer(0x8)
		ptr = cast(pSecInfoBuffer, POINTER(c_int))
		sec_addr = c_int(ptr[0])
		getSecDescr_status = windll.advapi32.GetSecurityDescriptorDacl(
			sec_addr,
			byref(pb1),
			byref(pSecDescrDACL),
			byref(pb3)
		)

		# allocamos memoria suficiente como para copiar la dacl y dos DWORDS mas
		# (al incicio de este), el tamanyo de bloque esta en [pSecDescrDACL + 2]
		ptr = cast(pSecDescrDACL, POINTER(c_int))
		sec_descr_addr = c_int(ptr[0])

		len_addr = c_int()
		len_addr.value = sec_descr_addr.value
		len_addr.value += 2

		tmp_buffer = create_string_buffer(0x8)
		length = cdll.msvcrt.memcpy(byref(tmp_buffer), len_addr.value, 1)
		final_len = cast(tmp_buffer, POINTER(c_int))
		final_len = c_int(final_len[0])
		malloc_addr = cdll.msvcrt.malloc(final_len)

		malloc_copy_addr = cdll.msvcrt.memcpy(malloc_addr, sec_descr_addr.value, final_len)

		# ahora vendria EqualSid:
		# sidMasOcho.value == len(SID)+0x8 [que copiamos en malloc_sidMasOcho]
		# sumamos sidMasOcho.value + final_len.value y reubicamos el buffer
		realloc_len = c_int()
		realloc_len.value = sidMasOcho.value + final_len.value
		realloc_base = cdll.msvcrt.realloc(malloc_copy_addr, realloc_len.value)
		
		# aumenta el tamanyo en la zona reallocada
		ptr_realloc = c_int()
		ptr_realloc.value = realloc_base+2
		realloc_len_ptr = c_int(realloc_len.value)
		malloc_copy_addr = cdll.msvcrt.memcpy(ptr_realloc, pointer(realloc_len), 1)

		# de aqui nos vamos a AddAce
		final_address = malloc_copy_addr-2
		addAce_status = windll.advapi32.AddAce(
			final_address,
			0x2,
			0x0,
			byref(malloc_sidMasOcho),
			0x24
		)

		# validamos la Acl
		validAcl = windll.advapi32.IsValidAcl(final_address)

		# queda SetSecurityAccessMask
		access_mask = create_string_buffer(0x8)
		#access_mask = c_void_p()
		set_access_mask = windll.advapi32.SetSecurityAccessMask(0x4, byref(access_mask))

		# despues ORea la mascara:
		#
		# Quedando:
		#
		# OR 00040000, 20000 == 00060000
		#
		# valor que volvemos a modificar:
		#
		# ACCESS_MASK |= OTHER_MASK (OR 0x60000, 0x80)
		# que lo pasa a la NtOpenFile:
		#
		# dereferenciamos el puntero, lo OReamos y lo ANDeamos
		FIRST_MASK = 0x04000000
		FIRST_MASK >>= 1
		FIRST_MASK = ~FIRST_MASK
		FIRST_MASK &= 0x80

		mask = cast(access_mask, POINTER(c_int))
		mask = c_int(mask[0])
		mask.value |= 0x20000
		mask.value |= FIRST_MASK

		#volvemos a abrir el archivo, esta vez con la nueva mascara de seguridad
		ntopen_status = windll.ntdll.NtOpenFile(
			byref(ret_handle),
			mask.value,
			byref(nt_buffer),
			byref(pStatusBlock),
			0x7,
			0x00200000
		)
		ptr = cast(ret_handle, POINTER(c_int))
		handle = c_int(ptr[0])

		# Vamos a ADVAPI32.SetSecurityInfo
		final_work = windll.advapi32.SetSecurityInfo(handle,
			0x1,
			0x4,
			0x0,
			0x0,
			final_address,
			0x0
		)

		# debe ser EAX==0x0(ALL_OK) Si todo fue bien
		if (final_work==0):
			print "  Status: Ok!"
		else:
			print "  Status: Error!"


	def existsFile( self, filename ):
		exists = windll.kernel32.CreateFileW(
			c_wchar_p(filename),
			0,
			1,
			0,
			3,
			80,
			0
		)
		existe = (exists != -1)
		windll.kernel32.CloseHandle(exists)
		return existe

def showUsage():
    sys.__stderr__.write(
    """ uso: %s archivo
     -archivo: ruta absoluta al archivo.

     @Ejemplo: python %s syxe c:\miArchivo.txt
               python %s Administrador c:\\ejecutame.exe
                        """%(sys.argv[0],sys.argv[0],sys.argv[0]))

def printheader():
    print "\n GainAccessX v1.0 - Utilidad para ganar acceso a un archivo"
    print " The Fast Lane (c) 2018 - SyXe'05[cls]"
    print " syxe05@gmail.com\n"

if __name__ == '__main__':
	printheader()
	a = sys.argv[1:]
	if (a.__len__() != 2):
		showUsage()
		sys.exit(1)
	else:
		user = a[0]
		filename = a[1]
		ga = GainAccess()
		ga.grantFullAccess( user, filename )
		