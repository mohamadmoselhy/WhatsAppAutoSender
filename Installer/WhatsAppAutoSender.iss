#define MyAppName "WhatsApp Auto Sender"
#define MyAppVersion "1.0"
#define MyAppPublisher "Mohamed Moselhy"
#define MyAppExeName "WhatsAppAutoSender.exe"

[Setup]
AppId={{YOUR-GUID-HERE}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=dist
OutputBaseFilename=WhatsAppAutoSender_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
SetupIconFile=..\resources\icon.ico

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "..\dist\WhatsAppAutoSender.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\dist\MessageTemplates\*"; DestDir: "{app}\MessageTemplates"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\resources\*"; DestDir: "{app}\resources"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\resources\icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\icon.ico"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\icon.ico"

[Code]
var
  RootPathPage, FolderToWatchPage, MainWatchFolderNamePage: TInputQueryWizardPage;

procedure InitializeWizard;
begin
  // Request DEFAULT_ROOT_PATH
  RootPathPage := CreateInputQueryPage(wpWelcome, 'Root Path', 'Please enter the DEFAULT_ROOT_PATH:', 'This is the root SharePoint or network path.');
  RootPathPage.Add('DEFAULT_ROOT_PATH:', False);
  RootPathPage.Values[0] := 'https://your.sharepoint.com/path';

  // Request DEFAULT_FOLDER_TO_WATCH
  FolderToWatchPage := CreateInputQueryPage(RootPathPage.ID, 'Folder to Watch', 'Please enter the DEFAULT_FOLDER_TO_WATCH:', 'This is the local folder to monitor for new files.');
  FolderToWatchPage.Add('DEFAULT_FOLDER_TO_WATCH:', False);
  FolderToWatchPage.Values[0] := 'C:\Users\YourName\Documents\WatchFolder';

  // Request MAIN_WATCH_FOLDER_NAME
  MainWatchFolderNamePage := CreateInputQueryPage(FolderToWatchPage.ID, 'Main Watch Folder Name', 'Please enter the MAIN_WATCH_FOLDER_NAME:', 'This is the main folder name used for contact extraction.');
  MainWatchFolderNamePage.Add('MAIN_WATCH_FOLDER_NAME:', False);
  MainWatchFolderNamePage.Values[0] := 'منظورة تجربة';
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    SaveStringToFile(ExpandConstant('{app}\.env'),
      'DEFAULT_ROOT_PATH=' + RootPathPage.Values[0] + #13#10 +
      'DEFAULT_FOLDER_TO_WATCH=' + FolderToWatchPage.Values[0] + #13#10 +
      'MAIN_WATCH_FOLDER_NAME=' + MainWatchFolderNamePage.Values[0] + #13#10,
      False);
  end;
end; 