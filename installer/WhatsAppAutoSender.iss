#define MyAppName "WhatsApp Auto Sender"
#define MyAppVersion "1.0"
#define MyAppPublisher "Mohamed Moselhy"
#define MyAppPublisherURL "mailto:Mohamed_Moselhy@outlook.com"
#define MyAppSupportURL "mailto:Mohamed_Moselhy@outlook.com"
#define MyAppUpdatesURL "mailto:Mohamed_Moselhy@outlook.com"
#define MyAppExeName "WhatsAppAutoSender.exe"
#define MyAppCopyright "Copyright © 2024 Mohamed Moselhy"
#define MyAppContact "Mohamed_Moselhy@outlook.com"

[Setup]
AppId={{B5A3E1D2-C8F4-4A9B-9E7D-6C3B2A1F0E9D}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppPublisherURL}
AppSupportURL={#MyAppSupportURL}
AppUpdatesURL={#MyAppUpdatesURL}
AppCopyright={#MyAppCopyright}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=..\LICENSE
OutputDir=..\dist
OutputBaseFilename=WhatsAppAutoSender-Setup
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
SetupLogging=yes
DisableProgramGroupPage=no
DisableWelcomePage=no
DisableReadyPage=no
DisableFinishedPage=no
SetupIconFile=..\resources\icon.ico
UninstallDisplayIcon={app}\icon.ico
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
CloseApplications=yes
RestartApplications=no
AlwaysRestart=no
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Messages]
WelcomeLabel2=This will install [name/ver] on your computer.%n%nThis application allows you to automatically send WhatsApp messages to groups based on file changes.%n%nDeveloped by: {#MyAppPublisher}%nContact: {#MyAppContact}
FinishedLabel=Setup has finished installing [name] on your computer.%n%nPlease refer to the documentation in the installation folder for usage instructions.

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "startmenuicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "autostart"; Description: "Start automatically with Windows"; GroupDescription: "Startup Options:"; Flags: unchecked

[Files]
Source: "..\dist\WhatsAppAutoSender.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\dist\MessageTemplates\*"; DestDir: "{app}\MessageTemplates"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\docs\Solution_Manual.md"; DestDir: "{app}\docs"; Flags: ignoreversion
Source: "..\resources\icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Dirs]
Name: "{app}\logs"; Flags: uninsneveruninstall

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\icon.ico"
Name: "{group}\User Manual"; Filename: "{app}\docs\Solution_Manual.md"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\icon.ico"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\icon.ico"; Tasks: startmenuicon
Name: "{userstartup}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\icon.ico"; Tasks: autostart

[Registry]
Root: HKCU; Subkey: "Software\{#MyAppPublisher}\{#MyAppName}"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\{#MyAppPublisher}\{#MyAppName}"; ValueType: string; ValueName: "InstallPath"; ValueData: "{app}"
Root: HKCU; Subkey: "Software\{#MyAppPublisher}\{#MyAppName}"; ValueType: string; ValueName: "Version"; ValueData: "{#MyAppVersion}"

[Code]
var
  WhatsAppGroupPage: TInputQueryWizardPage;
  FolderPage: TInputDirWizardPage;
  IntervalPage: TInputQueryWizardPage;

procedure InitializeWizard;
begin
  // Create custom page for WhatsApp group name
  WhatsAppGroupPage := CreateInputQueryPage(wpWelcome,
    'WhatsApp Group Configuration',
    'Please enter the WhatsApp group details',
    'Please specify the name of the WhatsApp group where messages will be sent.');
  WhatsAppGroupPage.Add('Group Name:', False);

  // Create custom page for message interval
  IntervalPage := CreateInputQueryPage(WhatsAppGroupPage.ID,
    'Message Interval Configuration',
    'Please enter the message check interval',
    'Specify how often (in seconds) the application should check for new messages.');
  IntervalPage.Add('Interval (seconds):', False);
  IntervalPage.Values[0] := '300';

  // Create custom page for folder selection
  FolderPage := CreateInputDirPage(IntervalPage.ID,
    'Select Folder to Monitor',
    'Please select the folder that will be monitored for new files:',
    'Select the folder to monitor for new files, then click Next.' + #13#10 + #13#10 +
    'This folder will be checked for new files that trigger WhatsApp messages.',
    False, '');
  FolderPage.Add('');
  FolderPage.Values[0] := ExpandConstant('{userdocs}');
end;

function IsValidInterval(const Value: String): Boolean;
var
  Interval: Integer;
begin
  Result := True;
  try
    Interval := StrToInt(Value);
    if (Interval < 60) or (Interval > 3600) then
      Result := False;
  except
    Result := False;
  end;
end;

function NextButtonClick(CurPageID: Integer): Boolean;
var
  FolderPath: String;
  GroupName: String;
begin
  Result := True;
  
  if CurPageID = WhatsAppGroupPage.ID then
  begin
    GroupName := WhatsAppGroupPage.Values[0];
    if GroupName = '' then
    begin
      MsgBox('Please enter a WhatsApp group name.', mbError, MB_OK);
      Result := False;
    end;
  end
  else if CurPageID = IntervalPage.ID then
  begin
    if not IsValidInterval(IntervalPage.Values[0]) then
    begin
      MsgBox('Please enter a valid interval between 60 and 3600 seconds.', mbError, MB_OK);
      Result := False;
    end;
  end
  else if CurPageID = FolderPage.ID then
  begin
    FolderPath := FolderPage.Values[0];
    if not DirExists(FolderPath) then
    begin
      if MsgBox('The selected folder does not exist. Would you like to create it?', 
         mbConfirmation, MB_YESNO) = IDYES then
      begin
        try
          ForceDirectories(FolderPath);
        except
          MsgBox('Failed to create the folder. Please select a different location.', mbError, MB_OK);
          Result := False;
        end;
      end
      else
        Result := False;
    end;
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  ConfigFile: String;
  ConfigContent: String;
begin
  if CurStep = ssPostInstall then
  begin
    // Create .env file with all configurations
    ConfigFile := ExpandConstant('{app}\.env');
    ConfigContent := 'WHATSAPP_GROUP_NAME=' + WhatsAppGroupPage.Values[0] + #13#10 +
                    'MESSAGE_INTERVAL=' + IntervalPage.Values[0] + #13#10 +
                    'FOLDER_TO_WATCH=' + FolderPage.Values[0] + #13#10 +
                    'APP_VERSION=' + '{#MyAppVersion}' + #13#10 +
                    'DEVELOPER=' + '{#MyAppPublisher}' + #13#10 +
                    'SUPPORT_EMAIL=' + '{#MyAppContact}';
    SaveStringToFile(ConfigFile, ConfigContent, False);
  end;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  case CurUninstallStep of
    usUninstall:
      begin
        // Optional: Delete any additional files or settings
      end;
    usPostUninstall:
      begin
        // Optional: Clean up any remaining files
      end;
  end;
end; 