import sys
from ctypes import *
from EnablePriv import *

__all__ = ["EnableAllPrivs"]

class EnableAllPrivs:
	ERROR_VALUE = -1
	#
	# List of available privileges
	#
	privileges = ("SeBackupPrivilege",
				  "SeChangeNotifyPrivilege",
				  "SeCreateGlobalPrivilege",
				  "SeCreatePagefilePrivilege",
				  "SeCreateSymbolicLinkPrivilege",
				  "SeDebugPrivilege",
				  "SeImpersonatePrivilege",
				  "SeIncreaseBasePriorityPrivilege",
				  "SeIncreaseQuotaPrivilege",
				  "SeIncreaseWorkingSetPrivilege",
				  "SeLoadDriverPrivilege",
				  "SeManageVolumePrivilege",
				  "SeProfileSingleProcessPrivilege",
				  "SeRemoteShutdownPrivilege",
				  "SeRestorePrivilege",
				  "SeSecurityPrivilege",
				  "SeShutdownPrivilege",
				  "SeSystemEnvironmentPrivilege",
				  "SeSystemProfilePrivilege",
				  "SeSystemtimePrivilege",
				  "SeTakeOwnershipPrivilege",
				  "SeTimeZonePrivilege",
				  "SeUndockPrivilege"
	)

	def enable(self):
		#print " EnableAllPrivs.enable()"
		e_priv = EnablePriv()
		for x in self.privileges:
			e_priv.enable(e_priv.getCurrentToken(), c_wchar_p(x))

	def enableForProcess(self, pid):
		#print " EnableAllPrivs.enableForProcess(%s)"%pid
		e_priv = EnablePriv()
		token = e_priv.getToken(pid)
		for x in self.privileges:
			e_priv.enable(token, c_wchar_p(x))

def showUsage():
    sys.__stderr__.write(
    """ uso: %s archivo
     -p: pid del proceso.

     @Ejemplo: python %s -p 0x114
               python %s 
                        """%(sys.argv[0],sys.argv[0],sys.argv[0]))

def printheader():
    print "\n EnableAllPrivsX v1.0 - Utilidad para habilitar privilegios en un proceso"
    print " The Fast Lane (c) 2018 - SyXe'05[cls]"
    print " syxe05@gmail.com\n"

if __name__ == '__main__':
	printheader()
	a = sys.argv[1:]
	if (a.__len__() == 0):
		# for current process
		print " Enabling: Current Process"
		enabler = EnableAllPrivs()
		status = enabler.enableForProcess(c_int(windll.kernel32.GetCurrentProcessId()).value)
		if status  != enabler.ERROR_VALUE:
			print "   Status: Ok!"
		else:
			print "   Status: Error!"
	elif (a.__len__() == 1):
		try:
			val = c_int(eval(a[0])).value
			print " Enabling: Pid", a[0]
			enabler = EnableAllPrivs()
			status = enabler.enableForProcess(val)
			if status  != enabler.ERROR_VALUE:
				print "   Status: Ok!"
			else:
				print "   Status: PID not found!"
		except:
			print "   Status: Error!"
	else:
		showUsage()
		sys.exit(1)
