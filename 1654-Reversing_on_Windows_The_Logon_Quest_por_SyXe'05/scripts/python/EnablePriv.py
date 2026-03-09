import struct
from ctypes import *

__all__ = ["EnablePriv"]

class TOKEN_PRIVILEGE(Structure):
	_fields_ = [
	    ("privilegeCount", c_char_p),
		("privilege_luid", c_char_p),
		("zeros", c_char_p),
		("SE_PRIVILEGE_ENABLED", c_char_p)]

class EnablePriv:
	pid = 0
	token = 0
	ERROR_VALUE = -1

	def enable(self, token, priv_name):
		pRetLen = c_void_p()
		ntstatus_gti = windll.advapi32.GetTokenInformation(
			token,
			1,
			0,
			0,
			byref(pRetLen)
		)

		if pRetLen.value == None:
			return self.ERROR_VALUE;

		heap = windll.kernel32.GetProcessHeap()
		heap_alloc = windll.kernel32.HeapAlloc(heap, pRetLen, pRetLen.value)

		mybuffer  = create_string_buffer(pRetLen.value)
		ntstatus_gti2 = windll.advapi32.GetTokenInformation(
			token,
			1,
			byref(mybuffer),
			sizeof(mybuffer),
			byref(pRetLen)
		)
		
		tk = TOKEN_PRIVILEGE()
		tk.privilegeCount = struct.pack('<i4', 1)
		tk.privilege_luid = struct.pack('<i4', 0)
		tk.zeros = struct.pack('<i4', 0)
		tk.SE_PRIVILEGE_ENABLED = struct.pack('<i4', 2)

		tkbuffer = create_string_buffer(sizeof(tk))
		lookup_priv_luid = windll.advapi32.LookupPrivilegeValueW(
			0,
			priv_name,
			tk.privilege_luid
		)

		copied =cdll.msvcrt.memcpy(byref(tkbuffer, 0), tk.privilegeCount, 1)
		copied =cdll.msvcrt.memcpy(byref(tkbuffer, 4), tk.privilege_luid, 1)
		copied =cdll.msvcrt.memcpy(byref(tkbuffer, 8), tk.zeros, 1)
		copied =cdll.msvcrt.memcpy(byref(tkbuffer, 0xC), tk.SE_PRIVILEGE_ENABLED, 1)

		adjust_priv = windll.advapi32.AdjustTokenPrivileges(
			token,
			0,
			tkbuffer,
			0x10,
			0,
			0
		)
		return adjust_priv

	def getCurrentToken(self):
		pid = windll.kernel32.GetCurrentProcessId()
		return self.getToken(windll.kernel32.GetCurrentProcessId())


	def getToken(self, pid):
		handle_process = windll.kernel32.OpenProcess(0x400, 0, pid)
		phToken = c_int()
		handle_token_status = windll.kernel32.OpenProcessToken(
			handle_process,
			0x28,
			byref(phToken)
		)
		ntstatus = windll.ntdll.ZwClose(handle_process)
		return phToken