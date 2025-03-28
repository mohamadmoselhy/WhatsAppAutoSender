@echo off

Set Mail_Username=madel.c
Set Mail_Password=xxxxxx
Set Mail_folder_name=Inbox
Set Mail_Sender=madel.c
Set Mail_Subject=test
Set Mail_PreviousHours=0
Set Orchestrator_TenantName=Default
Set OrchestratorProcessReleaseKey=7dc48847-8d3c-4a31-9f2b-c5330437ee5a
Set OrchestratorRobotID=248
Set OrchestratorMachineSessionID=413
Set OrchestratorFolderName=ProjectClosure
Set OrchestratorJobInputArguments={}
@echo on

"C:\Users\LENOVO\Desktop\EmailListener\Production\Exchange_EmailListener_StartJob.exe" "%Mail_Username%" "%Mail_Password%" "%Mail_folder_name%" "%Mail_Sender%" "%Mail_Subject%" "%Mail_PreviousHours%" "%Orchestrator_TenantName%" "%OrchestratorProcessReleaseKey%" "%OrchestratorRobotID%" "%OrchestratorMachineSessionID%" "%OrchestratorFolderName%" "%OrchestratorJobInputArguments%"