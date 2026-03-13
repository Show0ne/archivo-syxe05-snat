Option Explicit

' Public constants
Public Const DebugDisabled     = 0
Public Const DebugEnabled      = 1

Public Const InfiniteTimeout   = 0
Public Const InitalizerTimeout = 2
Public Const MessageTimeout    = 5
Public Const QuestionTimeout   = 10
Public Const LongTimeout       = 30

Public Const YesResponse       = 1
Public Const NoResponse        = 2

Public Const RegistryPath = "HKEY_CURRENT_USER\Volatile Environment\EnableDebug"
Public Const RegistryBoot = "HKEY_CURRENT_USER\Volatile Environment\BootDrive"
Public Const RegBootType  = "REG_SZ"
Public Const RegistryType = "REG_DWORD"

Public Const Habilitar    = "Habilitar"
Public Const Deshabilitar = "Deshabilitar"

' Variables
Dim iRetVal10
Dim oDebugging

' Object inicialization to avoid 424 Error!
Set oDebugging = New Debugging

'//----------------------------------------------------------------------------
'//  Debugging internal Class
'//----------------------------------------------------------------------------

Class Debugging

	'//----------------------------------------------------------------------------
	'//  Constructor to initialize needed global objects
	'//----------------------------------------------------------------------------
	
	Private Sub Class_Initialize
		If IsDebug Then
			oShell.Popup "IOCDebug.vbs Init By: " & oUtility.ScriptName, InitalizerTimeout, "Class Initializer", 64
		End If
	End Sub
	
	'//----------------------------------------------------------------------------
	'//  Main routine
	'//----------------------------------------------------------------------------

	Function Main
		'oShell.Popup "IOCDebug.vbs MAIN", 10, "IOCDebug.vbs Information", 60+4
	End Function
	
	
	Function AskUser(sStr)
	
		' Preguntamos si se quiere habilitar/deshabilitar la depuracion (con un timeout de 10 segundos)
		iRetVal10 = oShell.Popup(sStr & " la depuracion?", QuestionTimeout, "Atencion IOCDebug.vbs", 30+3)
		
		Select Case iRetVal10
		Case YesResponse And sStr = Habilitar
			oShell.RegWrite RegistryPath, DebugEnabled, RegistryType
			WriteLog "Debugging Enabled",LogTypeInfo
		Case YesResponse And sStr = Deshabilitar
			WriteLog "Disabling Debugging",LogTypeInfo
			oShell.RegWrite RegistryPath, DebugDisabled, RegistryType
		Case NoResponse And sStr = Habilitar
			WriteLog "Enable Debugging Rejected",LogTypeInfo
		Case NoResponse And sStr = Deshabilitar
			WriteLog "Disable Debugging Rejected",LogTypeInfo
		Case Else
			WriteLog "Unexpected Response: " & iRetVal10,LogTypeInfo
		End Select

		' Salimos
		AskUser = iRetVal10
	
	End Function


	Function IsDebug
	
		WriteLog "IsDebug called",LogTypeInfo
		
		Dim iStatus
		iStatus = FALSE
		
		On Error Resume Next
		iStatus = oShell.RegRead(RegistryPath)
		On Error Goto 0
		
		select Case iStatus
		Case "1"
			iStatus = TRUE
		Case Else
			iStatus = FALSE
		End Select
			
		WriteLog "IsDebug RETURNS " & iStatus,LogTypeInfo
		IsDebug = iStatus
		
	End Function
	
	
	Function SetDebug(sParam)
	
		WriteLog "SetDebug called with Arg: " & sParam, LogTypeInfo
		oShell.RegWrite RegistryPath, sParam, RegistryType
		
	End Function

	
	Function WriteLog(sData,sType)

		select Case sType
		Case LogTypeInfo, LogTypeWarning, LogTypeError, LogTypeVerbose
			oLogging.CreateEntry "   ===== IOCDebug " & sData & " =====   ", sType
		Case Else
			' Recursive case, sType MUST BE VALID to avoid an infinite loop!
			WriteLog "IOCDebug WriteLog INVALID TYPE " & sType, LogTypeInfo
		End Select

	End Function
	
	
	Function ShowMessage(sMsg,sTimeout,sTitle)

		If Not IsDebug Then
			' Avisamos del incidente vía 'C:\Windows\Temp\DeploymentLogs\Results.xml'
			WriteLog "ShowMessage called from " & oUtility.ScriptName & " while NOT DEBUGING", LogTypeInfo
		Else
			oShell.Popup sMsg, sTimeout, sTitle, 60+4
		End If
	
	End Function
	
End Class
