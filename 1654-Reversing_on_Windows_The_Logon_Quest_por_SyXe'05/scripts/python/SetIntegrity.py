
from GetIntegrity import *

class OBJECT_ATTRIBUTES(Structure):
	_fields_ = [
	    ("Length", c_char_p),
		("RootDirectory", c_char_p),
		("ObjectName", c_char_p),
		("Attributes", c_char_p),
		("SecurityDescriptor", c_char_p),
		("SecurityQualityOfService", c_char_p)]

class Integrity:

	integrities = (0x1000, 0x2000, 0x3000)
	integrities0 = ("LOW", "MEDIUM", "HIGH")
	BAD_INTEGRITY_VALUE = 0x0
	displayIntegrity = ''

	def setIntegrityLevel( self, filename, integrityType ):
		print "  File:", filename.value
		getIntegrity = GetIntegrity()
		i = getIntegrity.getIntegrityLevel(filename)
		print " nuevo:", integrityType.value
		
		# primera llamada a ADVAPI32.ConvertStringSidToSidW que toma 2 parametros:
		#
		#	arg1: ptr escribible
		#	arg2: UNICODE_STRING (HI, ME, LW)
		#
		# definimos un alias para las librerias
		advapi = windll.advapi32
		kernel = windll.kernel32
		msvcrt = cdll.msvcrt
		ntdll  = windll.ntdll

		pSid = create_string_buffer(0x40)
		status_code = advapi.ConvertStringSidToSidW(integrityType, pSid)

		# si todo fue bien deberia ser status_code == 0x1(ALL_OK)
		if (status_code != 0x1):
			print " Error: al Convertir la Sid '%s'"%integrityType.value
			return

		# con todo correcto vamos a derreferenciar el puntero y llamamos
		#  a LocalSize que retornara en EAX el valor
		puntero = cast(pSid, POINTER(c_int))
		sid_addr = c_int(cast(pSid, POINTER(c_int))[0])
		local_size = kernel.LocalSize(sid_addr)

		# con este size llamamos a malloc
		malloc_sacl = msvcrt.malloc(local_size)

		# copiamos la Sid a otro buffer
		status_code = advapi.CopySid(local_size, malloc_sacl, sid_addr)

		# si va todo bien retorna EAX==0x1(ALL_OK)
		if (status_code != 0x1):
			print " Error: al Copiar la Sid, abortando.."
			return

		#liberamos la region de memoria
		status_code = kernel.LocalFree(pSid)


		# Obtenemos el tamanyo de la Sid que retornara en EAX
		len_sid = advapi.GetLengthSid(malloc_sacl)

		# reservamos un buffer de len_sid + 0x8
		sidMasOcho = len_sid + 8

		# Reservamos un buffer de este tamanyo
		malloc_sidMasOcho = msvcrt.malloc(sidMasOcho)

		# Ahora hay que copiar algunos valores en este buffer recien creado
		#
		#	mov byte ptr [buffer], 0x11
		#	mov byte ptr [buffer + 0x1], 0x0
		#	mov dword ptr [buffer + 0x4], 0x1
		#	mov word ptr [buffer + 0x2], sidMasOcho
		#
		msvcrt.memcpy(malloc_sidMasOcho, pointer(c_int(0x11)), 1)
		msvcrt.memcpy(malloc_sidMasOcho+0x1, pointer(c_int(0x0)), 1)
		msvcrt.memcpy(malloc_sidMasOcho+0x4, pointer(c_int(0x1)), 4)
		msvcrt.memcpy(malloc_sidMasOcho+0x2, pointer(c_int(sidMasOcho)), 2)

		# despues copiamos 0xC bytes de pSid a buffer+0x8
		msvcrt.memcpy(malloc_sidMasOcho+0x8, malloc_sacl, len_sid)

		# Y nos queda esta estructura en memoria:
		#
		# 	00xxxxxx    11 00 14 00 01 00 00 00  ........
		# 	00yyyyyy    01 01 00 00 00 00 00 10  ........
		# 	00zzzzzz    00 10 00 00 AB AB AB AB  ........
		#
		# Llamamos a GetFileAttributes y comparamos el retorno, si es -0x1
		# indicamos el error y salimos del programa
		status_code = kernel.GetFileAttributesW(filename)
		if (status_code == -1):
			print "File attributes ERROR!"
			return 1

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

		# salvamos la direccion de la cadena en nuestra estructura
		nt_struct.ObjectName = struct.pack('<i4', addressof(UNICODE_STRING))

		# Y la pasamos a un buffer
		nt_buffer = create_string_buffer(sizeof(nt_struct))

		msvcrt.memcpy(byref(nt_buffer, 0), nt_struct.Length, 1)
		msvcrt.memcpy(
			byref(nt_buffer, 4),
			nt_struct.RootDirectory,
			len(nt_struct.RootDirectory)
        )
		msvcrt.memcpy(byref(nt_buffer, 8), nt_struct.ObjectName, 4)
		msvcrt.memcpy(byref(nt_buffer, 0xC), nt_struct.Attributes, 1)
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

		# dereferenciamos el handle
		puntero = cast(ret_handle, POINTER(c_int))
		handle = c_int(puntero[0])

        # Si hay error lo indicamos yu salimos
		if (handle.value == 0x0):
			print " Error: no es posible abrir %s"%filename
			return -1

		# Vamos a ZwQueryInformationFile
		pAuxBuffer = create_string_buffer(0x8)
		status_code = ntdll.ZwQueryInformationFile(
			handle,
			byref(pAuxBuffer),
			byref(pStatusBlock),
			0x23,
			0x8
	    )

		# si la llamada tiene exito retorna EAX==0x0(ALL_OK)
		# Deberiamos testear el resultado:
		#
		#	00xxxxxx  test    dword ptr [ebp-14], 400
		#	00yyyyyy  je      short 00zzzzzz
		#
		# Y seguimos por GetSecurityInfo
		pSecurityInfo = create_string_buffer(0x100)
		status_code = windll.advapi32.GetSecurityInfo(
			handle,
			0x1,
			0x17,
			0x0,
			0x0,
			0x0,
			0x0,
			byref(pSecurityInfo)
		)

		# si la llamada tiene exito retorna EAX==0x0(ALL_OK)
		if (status_code != 0x0):
			print " Error obteneniendo informacion de seguridad para '%s'"%filename.value
			return -1
		# Ahora cerramos el manejador de archivo
		status_code = kernel.CloseHandle(handle)
		# si la llamada tiene exito retorna EAX==0x1(ALL_OK)

		# Vamos a ADVAPI32.GetSecurityDescriptorDacl
		# Antes dereferenciamos los punteros que necesitamos y creamos bloques 
		# de memoria que se van a utilizar en la siguiente llamada
		pDACL = create_string_buffer(0x64)
		pAuxBuffer2 = create_string_buffer(0x8)
		puntero = cast(pSecurityInfo, POINTER(c_int))
		securityInfo = c_int(puntero[0])
		status_code = windll.advapi32.GetSecurityDescriptorDacl(
			securityInfo,
			byref(pAuxBuffer),
			byref(pDACL),
			byref(pAuxBuffer2)
		)

		# si la llamada tiene exito retorna EAX==0x1(ALL_OK)
		if (status_code != 0x1):
			print " Error obteneniendo informacion de seguridad para '%s'"%filename.value
			return -1

		# Y vamos operando con los resultados, sobretodo con la DACL
		#
		# 	Obtenemos su longitud que esta en pDacl+0x2
		#
		# allocamos memoria suficiente como para copiar la dacl y dos DWORDS
		#  mas (al incicio de este), el tamanyo de bloque esta en [pDACL + 2]
		dacl_addr = cast(pDACL, POINTER(c_int))[0]
		dacl_len_offset = dacl_addr + 0x2
		dacl_len_addr = cast(byref(c_int(dacl_len_offset)), POINTER(c_int))[0]
		dacl_len = cast(dacl_len_addr, POINTER(c_byte))[0]
		pDacl_malloc = cdll.msvcrt.malloc(dacl_len)

		# tenemos el tamany, vamos a malloc
		# copiamos la Dacl a un buffer
		#
		# void * _Cdecl memcpy(void *__dest, const void *__src, size_t __n);
		dacl_copy_addr = cdll.msvcrt.memcpy(pDacl_malloc, dacl_addr, dacl_len)

		# Liberamos el bloque 'securityInfo'
		free_secInfo = kernel.LocalFree(securityInfo)
		sacl_len_offset = malloc_sidMasOcho + 0x2
		sacl_len = cast(sacl_len_offset, POINTER(c_byte))[0]
		malloc_for_sacl=create_string_buffer(sacl_len + 0x8)

		# Inicializamos la ACL en este espacio de memoria
		initACL = advapi.InitializeAcl(malloc_for_sacl, (sacl_len + 0x8),0x2)

		# Retornara EAX==0x1(ALL_OK) si todo fue bien
		if (initACL != 0x1):
			print " Error inicializando la ACL"
			return -1

		# insertamos la ACE en esta ACL
		addAce_status = advapi.AddAce(
			byref(malloc_for_sacl),
			0x2,
			0x0,
			malloc_sidMasOcho,
			sacl_len
		)

		# si la llamada tiene exito retorna EAX==0x1(ALL_OK)
		if (addAce_status != 0x1):
			print " Error agregando la ACE"
			return -1

		# comprobamos que la ACL resultante sea valida, ojo la DACL (no la SACL):
		isValidAcl = advapi.IsValidAcl(pDacl_malloc)

		# si la llamada tiene exito retorna EAX==0x0(ALL_OK)
		if (isValidAcl != 0x1):
			print " Error de formato de ACL"
			return -1

		# Vamos a SetSecurityAccessMask
		access_mask = create_string_buffer(0x4)
		set_access_mask = windll.advapi32.SetSecurityAccessMask(
			0x14,
			byref(access_mask)
		)

		# preparamos la mascara de acceso
		FIRST_MASK = 0x04000000
		FIRST_MASK >>= 1
		FIRST_MASK = ~FIRST_MASK
		FIRST_MASK &= 0x80

		mask = cast(access_mask, POINTER(c_int))
		mask = c_int(mask[0])
		mask.value |= 0x20000
		mask.value |= FIRST_MASK

		#volvemos a abrir el archivo, esta vez con la nueva mascara de seguridad
		ntopen_status = ntdll.NtOpenFile(
			byref(ret_handle),
			mask.value,
			byref(nt_buffer),
			byref(pStatusBlock),
			0x7,
			0x200000
		)

		ptr = cast(ret_handle, POINTER(c_int))
		handle = c_int(ptr[0])

		# omprobamos el handle.
		if (handle.value == 0x0):
			print " Error de acceso a '%s' con ACCESS_MASK==0x%X"%(filename.value,mask.value)
			return -1

		# Aplicamos la informacion en el archivo
		final_status = windll.advapi32.SetSecurityInfo(
			handle,
			0x1,
			0x14,
			0x0,
			0x0,
			pDacl_malloc,
			malloc_for_sacl
		)

        # cerramos el handle y comprobamos el status de la operacion.
		close_status = windll.kernel32.CloseHandle(handle)
		if (final_status == 0x0):
			print " Final: nuevos atributos establecidos."
		else:
			print " Final: No se pudo establecer la informacion de seguridad en '%s'"%filename.value
		# si todo fue bien deberiamos obtener un status_code == 0x0(ALL_OK)
		# y el nuevo nivel de integridad estaria aplicado.


	def parseInterity( self, integrity ):
		#print "parsing intergrity: ", integrity
		if (integrity == self.integrities[0]) | (integrity == self.integrities0[0]):
			#print "LOW LEVEL"
			self.displayIntegrity = "LOW"
			return create_unicode_buffer("LW")
		elif (integrity == self.integrities[1]) | (integrity == self.integrities0[1]):
			#print "MEDIUM LEVEL"
			self.displayIntegrity = "MEDIUM"
			return create_unicode_buffer("ME")
		elif (integrity == self.integrities[2]) | (integrity == self.integrities0[2]):
			#print "HIGH LEVEL"
			self.displayIntegrity = "HIGH"
			return create_unicode_buffer("HI")
		else:
			return self.BAD_INTEGRITY_VALUE

def showUsage():
    sys.__stderr__.write(
    """ uso: %s [archivo, attribs]
     -archivo: ruta absoluta al archivo de trabajo.
     -attribs: Nuevo nivel de integridad a establecer
               Posibles {
                          LOW (0x1000),
                          MEDIUM (0x2000),
                          HIGH (0x3000)
                        }
     @Ejemplo: python %s c:\miArchivo.txt LOW
               python %s c:\otro_file.txt MEDIUM
               python %s c:\\ejecutame.exe HIGH
                        """%(sys.argv[0],sys.argv[0],sys.argv[0],sys.argv[0]))

def printheader():
    print "\n IntegrityX v1.0 - Utilidad para modificar el Nivel de Integridad"
    print " The Fast Lane (c) 2018 - SyXe'05[cls]"
    print " syxe05@gmail.com\n"



if __name__ == '__main__':
	printheader()
	integrity = Integrity()

	a = sys.argv[1:]
	if (a.__len__() != 2):
		showUsage()
		sys.exit(1)
		
	# hay que convertir la string a UNICODE
	filename = create_unicode_buffer(a[0])
	integrityType = integrity.parseInterity(a[1])
	if (integrityType==integrity.BAD_INTEGRITY_VALUE):
	    showUsage()
	    sys.exit(1)

	integrity.setIntegrityLevel(filename,integrityType)