; Script generated by the HM NIS Edit Script Wizard.

; HM NIS Edit Wizard helper defines
!define PRODUCT_NAME "NFT Card Manager"
!define PRODUCT_VERSION "1.1.0"
!define PRODUCT_PUBLISHER "Cryptnox SA"
!define PRODUCT_WEB_SITE "https://cryptnox.ch"
!define PRODUCT_DIR_REGKEY "Software\Microsoft\Windows\CurrentVersion\App Paths\NFT Card Manager.exe"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_UNINST_ROOT_KEY "HKLM"

SetCompressor lzma

; MUI 1.67 compatible ------
!include "MUI.nsh"

; MUI Settings
!define MUI_ABORTWARNING
!define MUI_ICON "cryptnox.ico"
!define MUI_UNICON "cryptnox.ico"

; Welcome page
!insertmacro MUI_PAGE_WELCOME
; License page
!insertmacro MUI_PAGE_LICENSE "LICENSE"
; Directory page
!insertmacro MUI_PAGE_DIRECTORY
; Instfiles page
!insertmacro MUI_PAGE_INSTFILES
; Finish page
!define MUI_FINISHPAGE_RUN "$INSTDIR\NFT Card Manager.exe"
!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_INSTFILES

; Language files
!insertmacro MUI_LANGUAGE "English"

; Reserve files
!insertmacro MUI_RESERVEFILE_INSTALLOPTIONS

; MUI end ------

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "NFTCardManager-setup.exe"
InstallDir "$PROGRAMFILES\NFT Card Manager"
InstallDirRegKey HKLM "${PRODUCT_DIR_REGKEY}" ""
ShowInstDetails show
ShowUnInstDetails show

Section "MainSection" SEC01
  SetOutPath "$INSTDIR\aiohttp"
  SetOverwrite try
  File "dist\NFT Card Manager\aiohttp\_helpers.cp39-win_amd64.pyd"
  File "dist\NFT Card Manager\aiohttp\_http_parser.cp39-win_amd64.pyd"
  File "dist\NFT Card Manager\aiohttp\_http_writer.cp39-win_amd64.pyd"
  File "dist\NFT Card Manager\aiohttp\_websocket.cp39-win_amd64.pyd"
  SetOutPath "$INSTDIR"
  File "dist\NFT Card Manager\api-ms-win-core-console-l1-1-0.dll"
  File "dist\NFT Card Manager\api-ms-win-core-datetime-l1-1-0.dll"
  File "dist\NFT Card Manager\api-ms-win-core-debug-l1-1-0.dll"
  File "dist\NFT Card Manager\api-ms-win-core-errorhandling-l1-1-0.dll"
  File "dist\NFT Card Manager\api-ms-win-core-file-l1-1-0.dll"
  File "dist\NFT Card Manager\api-ms-win-core-file-l1-2-0.dll"
  File "dist\NFT Card Manager\api-ms-win-core-file-l2-1-0.dll"
  File "dist\NFT Card Manager\api-ms-win-core-handle-l1-1-0.dll"
  File "dist\NFT Card Manager\api-ms-win-core-heap-l1-1-0.dll"
  File "dist\NFT Card Manager\api-ms-win-core-interlocked-l1-1-0.dll"
  File "dist\NFT Card Manager\api-ms-win-core-libraryloader-l1-1-0.dll"
  File "dist\NFT Card Manager\api-ms-win-core-localization-l1-2-0.dll"
  File "dist\NFT Card Manager\api-ms-win-core-memory-l1-1-0.dll"
  File "dist\NFT Card Manager\api-ms-win-core-namedpipe-l1-1-0.dll"
  File "dist\NFT Card Manager\api-ms-win-core-processenvironment-l1-1-0.dll"
  File "dist\NFT Card Manager\api-ms-win-core-processthreads-l1-1-0.dll"
  File "dist\NFT Card Manager\api-ms-win-core-processthreads-l1-1-1.dll"
  File "dist\NFT Card Manager\api-ms-win-core-profile-l1-1-0.dll"
  File "dist\NFT Card Manager\api-ms-win-core-rtlsupport-l1-1-0.dll"
  File "dist\NFT Card Manager\api-ms-win-core-string-l1-1-0.dll"
  File "dist\NFT Card Manager\api-ms-win-core-synch-l1-1-0.dll"
  File "dist\NFT Card Manager\api-ms-win-core-synch-l1-2-0.dll"
  File "dist\NFT Card Manager\api-ms-win-core-sysinfo-l1-1-0.dll"
  File "dist\NFT Card Manager\api-ms-win-core-timezone-l1-1-0.dll"
  File "dist\NFT Card Manager\api-ms-win-core-util-l1-1-0.dll"
  File "dist\NFT Card Manager\api-ms-win-crt-conio-l1-1-0.dll"
  File "dist\NFT Card Manager\api-ms-win-crt-convert-l1-1-0.dll"
  File "dist\NFT Card Manager\api-ms-win-crt-environment-l1-1-0.dll"
  File "dist\NFT Card Manager\api-ms-win-crt-filesystem-l1-1-0.dll"
  File "dist\NFT Card Manager\api-ms-win-crt-heap-l1-1-0.dll"
  File "dist\NFT Card Manager\api-ms-win-crt-locale-l1-1-0.dll"
  File "dist\NFT Card Manager\api-ms-win-crt-math-l1-1-0.dll"
  File "dist\NFT Card Manager\api-ms-win-crt-multibyte-l1-1-0.dll"
  File "dist\NFT Card Manager\api-ms-win-crt-process-l1-1-0.dll"
  File "dist\NFT Card Manager\api-ms-win-crt-runtime-l1-1-0.dll"
  File "dist\NFT Card Manager\api-ms-win-crt-stdio-l1-1-0.dll"
  File "dist\NFT Card Manager\api-ms-win-crt-string-l1-1-0.dll"
  File "dist\NFT Card Manager\api-ms-win-crt-time-l1-1-0.dll"
  File "dist\NFT Card Manager\api-ms-win-crt-utility-l1-1-0.dll"
  File "dist\NFT Card Manager\base_library.zip"
  SetOutPath "$INSTDIR\certifi"
  File "dist\NFT Card Manager\certifi\cacert.pem"
  SetOutPath "$INSTDIR"
  File "dist\NFT Card Manager\cryptnox_transparent.png"
  SetOutPath "$INSTDIR\cryptography\hazmat\bindings"
  File "dist\NFT Card Manager\cryptography\hazmat\bindings\_openssl.pyd"
  File "dist\NFT Card Manager\cryptography\hazmat\bindings\_rust.pyd"
  SetOutPath "$INSTDIR\cryptography-36.0.2.dist-info"
  File "dist\NFT Card Manager\cryptography-36.0.2.dist-info\INSTALLER"
  File "dist\NFT Card Manager\cryptography-36.0.2.dist-info\LICENSE"
  File "dist\NFT Card Manager\cryptography-36.0.2.dist-info\LICENSE.APACHE"
  File "dist\NFT Card Manager\cryptography-36.0.2.dist-info\LICENSE.BSD"
  File "dist\NFT Card Manager\cryptography-36.0.2.dist-info\LICENSE.PSF"
  File "dist\NFT Card Manager\cryptography-36.0.2.dist-info\METADATA"
  File "dist\NFT Card Manager\cryptography-36.0.2.dist-info\RECORD"
  File "dist\NFT Card Manager\cryptography-36.0.2.dist-info\top_level.txt"
  File "dist\NFT Card Manager\cryptography-36.0.2.dist-info\WHEEL"
  SetOutPath "$INSTDIR\frozenlist"
  File "dist\NFT Card Manager\frozenlist\_frozenlist.cp39-win_amd64.pyd"
  SetOutPath "$INSTDIR"
  File "dist\NFT Card Manager\libcrypto-1_1.dll"
  File "dist\NFT Card Manager\libffi-7.dll"
  File "dist\NFT Card Manager\libssl-1_1.dll"
  File "dist\NFT Card Manager\MSVCP140.dll"
  SetOutPath "$INSTDIR\multidict"
  File "dist\NFT Card Manager\multidict\_multidict.cp39-win_amd64.pyd"
  SetOutPath "$INSTDIR"
  File "dist\NFT Card Manager\NFT Card Manager.exe"
  CreateDirectory "$SMPROGRAMS\NFT Card Manager"
  CreateShortCut "$SMPROGRAMS\NFT Card Manager\NFT Card Manager.lnk" "$INSTDIR\NFT Card Manager.exe"
  CreateShortCut "$DESKTOP\NFT Card Manager.lnk" "$INSTDIR\NFT Card Manager.exe"
  File "dist\NFT Card Manager\nft_display.py"
  File "dist\NFT Card Manager\pyexpat.pyd"
  File "dist\NFT Card Manager\python3.dll"
  File "dist\NFT Card Manager\python39.dll"
  File "dist\NFT Card Manager\select.pyd"
  SetOutPath "$INSTDIR\smartcard\scard"
  File "dist\NFT Card Manager\smartcard\scard\_scard.cp39-win_amd64.pyd"
  SetOutPath "$INSTDIR"
  File "dist\NFT Card Manager\ucrtbase.dll"
  File "dist\NFT Card Manager\unicodedata.pyd"
  File "dist\NFT Card Manager\VCRUNTIME140.dll"
  SetOutPath "$INSTDIR\wx\lib\pubsub\core\arg1"
  File "dist\NFT Card Manager\wx\lib\pubsub\core\arg1\listenerimpl.py"
  File "dist\NFT Card Manager\wx\lib\pubsub\core\arg1\publisher.py"
  File "dist\NFT Card Manager\wx\lib\pubsub\core\arg1\publishermixin.py"
  File "dist\NFT Card Manager\wx\lib\pubsub\core\arg1\topicargspecimpl.py"
  File "dist\NFT Card Manager\wx\lib\pubsub\core\arg1\topicmgrimpl.py"
  File "dist\NFT Card Manager\wx\lib\pubsub\core\arg1\__init__.py"
  SetOutPath "$INSTDIR\wx\lib\pubsub\core"
  File "dist\NFT Card Manager\wx\lib\pubsub\core\callables.py"
  File "dist\NFT Card Manager\wx\lib\pubsub\core\imp2.py"
  File "dist\NFT Card Manager\wx\lib\pubsub\core\itopicdefnprovider.py"
  SetOutPath "$INSTDIR\wx\lib\pubsub\core\kwargs"
  File "dist\NFT Card Manager\wx\lib\pubsub\core\kwargs\datamsg.py"
  File "dist\NFT Card Manager\wx\lib\pubsub\core\kwargs\listenerimpl.py"
  File "dist\NFT Card Manager\wx\lib\pubsub\core\kwargs\publisher.py"
  File "dist\NFT Card Manager\wx\lib\pubsub\core\kwargs\publishermixin.py"
  File "dist\NFT Card Manager\wx\lib\pubsub\core\kwargs\topicargspecimpl.py"
  File "dist\NFT Card Manager\wx\lib\pubsub\core\kwargs\topicmgrimpl.py"
  File "dist\NFT Card Manager\wx\lib\pubsub\core\kwargs\__init__.py"
  SetOutPath "$INSTDIR\wx\lib\pubsub\core"
  File "dist\NFT Card Manager\wx\lib\pubsub\core\listener.py"
  File "dist\NFT Card Manager\wx\lib\pubsub\core\listenerbase.py"
  File "dist\NFT Card Manager\wx\lib\pubsub\core\notificationmgr.py"
  File "dist\NFT Card Manager\wx\lib\pubsub\core\publisherbase.py"
  File "dist\NFT Card Manager\wx\lib\pubsub\core\topicargspec.py"
  File "dist\NFT Card Manager\wx\lib\pubsub\core\topicdefnprovider.py"
  File "dist\NFT Card Manager\wx\lib\pubsub\core\topicexc.py"
  File "dist\NFT Card Manager\wx\lib\pubsub\core\topicmgr.py"
  File "dist\NFT Card Manager\wx\lib\pubsub\core\topicobj.py"
  File "dist\NFT Card Manager\wx\lib\pubsub\core\topictreetraverser.py"
  File "dist\NFT Card Manager\wx\lib\pubsub\core\topicutils.py"
  File "dist\NFT Card Manager\wx\lib\pubsub\core\treeconfig.py"
  File "dist\NFT Card Manager\wx\lib\pubsub\core\validatedefnargs.py"
  File "dist\NFT Card Manager\wx\lib\pubsub\core\weakmethod.py"
  File "dist\NFT Card Manager\wx\lib\pubsub\core\__init__.py"
  SetOutPath "$INSTDIR\wx\lib\pubsub"
  File "dist\NFT Card Manager\wx\lib\pubsub\policies.py"
  File "dist\NFT Card Manager\wx\lib\pubsub\pub.py"
  File "dist\NFT Card Manager\wx\lib\pubsub\py2and3.py"
  File "dist\NFT Card Manager\wx\lib\pubsub\setuparg1.py"
  File "dist\NFT Card Manager\wx\lib\pubsub\setupkwargs.py"
  SetOutPath "$INSTDIR\wx\lib\pubsub\utils"
  File "dist\NFT Card Manager\wx\lib\pubsub\utils\exchandling.py"
  File "dist\NFT Card Manager\wx\lib\pubsub\utils\misc.py"
  File "dist\NFT Card Manager\wx\lib\pubsub\utils\notification.py"
  File "dist\NFT Card Manager\wx\lib\pubsub\utils\topictreeprinter.py"
  File "dist\NFT Card Manager\wx\lib\pubsub\utils\xmltopicdefnprovider.py"
  File "dist\NFT Card Manager\wx\lib\pubsub\utils\__init__.py"
  SetOutPath "$INSTDIR\wx\lib\pubsub"
  File "dist\NFT Card Manager\wx\lib\pubsub\__init__.py"
  SetOutPath "$INSTDIR\wx"
  File "dist\NFT Card Manager\wx\siplib.cp39-win_amd64.pyd"
  File "dist\NFT Card Manager\wx\_adv.cp39-win_amd64.pyd"
  File "dist\NFT Card Manager\wx\_core.cp39-win_amd64.pyd"
  File "dist\NFT Card Manager\wx\_html.cp39-win_amd64.pyd"
  File "dist\NFT Card Manager\wx\_media.cp39-win_amd64.pyd"
  File "dist\NFT Card Manager\wx\_msw.cp39-win_amd64.pyd"
  SetOutPath "$INSTDIR"
  File "dist\NFT Card Manager\wxbase315u_net_vc140_x64.dll"
  File "dist\NFT Card Manager\wxbase315u_vc140_x64.dll"
  File "dist\NFT Card Manager\wxmsw315u_core_vc140_x64.dll"
  File "dist\NFT Card Manager\wxmsw315u_html_vc140_x64.dll"
  File "dist\NFT Card Manager\wxmsw315u_media_vc140_x64.dll"
  SetOutPath "$INSTDIR\yarl"
  File "dist\NFT Card Manager\yarl\_quoting_c.cp39-win_amd64.pyd"
  SetOutPath "$INSTDIR"
  File "dist\NFT Card Manager\_asyncio.pyd"
  File "dist\NFT Card Manager\_bz2.pyd"
  File "dist\NFT Card Manager\_cffi_backend.cp39-win_amd64.pyd"
  File "dist\NFT Card Manager\_ctypes.pyd"
  File "dist\NFT Card Manager\_decimal.pyd"
  File "dist\NFT Card Manager\_hashlib.pyd"
  File "dist\NFT Card Manager\_lzma.pyd"
  File "dist\NFT Card Manager\_multiprocessing.pyd"
  File "dist\NFT Card Manager\_overlapped.pyd"
  File "dist\NFT Card Manager\_queue.pyd"
  File "dist\NFT Card Manager\_socket.pyd"
  File "dist\NFT Card Manager\_ssl.pyd"
  File "dist\NFT Card Manager\_uuid.pyd"
SectionEnd

Section -AdditionalIcons
  CreateShortCut "$SMPROGRAMS\NFT Card Manager\Uninstall.lnk" "$INSTDIR\uninst.exe"
SectionEnd

Section -Post
  WriteUninstaller "$INSTDIR\uninst.exe"
  WriteRegStr HKLM "${PRODUCT_DIR_REGKEY}" "" "$INSTDIR\NFT Card Manager.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "$(^Name)"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\uninst.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayIcon" "$INSTDIR\NFT Card Manager.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
SectionEnd


Function un.onUninstSuccess
  HideWindow
  MessageBox MB_ICONINFORMATION|MB_OK "$(^Name) was successfully removed from your computer."
FunctionEnd

Function un.onInit
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "Are you sure you want to completely remove $(^Name) and all of its components?" IDYES +2
  Abort
FunctionEnd

Section Uninstall
  Delete "$INSTDIR\uninst.exe"
  Delete "$INSTDIR\_uuid.pyd"
  Delete "$INSTDIR\_ssl.pyd"
  Delete "$INSTDIR\_socket.pyd"
  Delete "$INSTDIR\_queue.pyd"
  Delete "$INSTDIR\_overlapped.pyd"
  Delete "$INSTDIR\_multiprocessing.pyd"
  Delete "$INSTDIR\_lzma.pyd"
  Delete "$INSTDIR\_hashlib.pyd"
  Delete "$INSTDIR\_decimal.pyd"
  Delete "$INSTDIR\_ctypes.pyd"
  Delete "$INSTDIR\_cffi_backend.cp39-win_amd64.pyd"
  Delete "$INSTDIR\_bz2.pyd"
  Delete "$INSTDIR\_asyncio.pyd"
  Delete "$INSTDIR\yarl\_quoting_c.cp39-win_amd64.pyd"
  Delete "$INSTDIR\wxmsw315u_media_vc140_x64.dll"
  Delete "$INSTDIR\wxmsw315u_html_vc140_x64.dll"
  Delete "$INSTDIR\wxmsw315u_core_vc140_x64.dll"
  Delete "$INSTDIR\wxbase315u_vc140_x64.dll"
  Delete "$INSTDIR\wxbase315u_net_vc140_x64.dll"
  Delete "$INSTDIR\wx\_msw.cp39-win_amd64.pyd"
  Delete "$INSTDIR\wx\_media.cp39-win_amd64.pyd"
  Delete "$INSTDIR\wx\_html.cp39-win_amd64.pyd"
  Delete "$INSTDIR\wx\_core.cp39-win_amd64.pyd"
  Delete "$INSTDIR\wx\_adv.cp39-win_amd64.pyd"
  Delete "$INSTDIR\wx\siplib.cp39-win_amd64.pyd"
  Delete "$INSTDIR\wx\lib\pubsub\__init__.py"
  Delete "$INSTDIR\wx\lib\pubsub\utils\__init__.py"
  Delete "$INSTDIR\wx\lib\pubsub\utils\xmltopicdefnprovider.py"
  Delete "$INSTDIR\wx\lib\pubsub\utils\topictreeprinter.py"
  Delete "$INSTDIR\wx\lib\pubsub\utils\notification.py"
  Delete "$INSTDIR\wx\lib\pubsub\utils\misc.py"
  Delete "$INSTDIR\wx\lib\pubsub\utils\exchandling.py"
  Delete "$INSTDIR\wx\lib\pubsub\setupkwargs.py"
  Delete "$INSTDIR\wx\lib\pubsub\setuparg1.py"
  Delete "$INSTDIR\wx\lib\pubsub\py2and3.py"
  Delete "$INSTDIR\wx\lib\pubsub\pub.py"
  Delete "$INSTDIR\wx\lib\pubsub\policies.py"
  Delete "$INSTDIR\wx\lib\pubsub\core\__init__.py"
  Delete "$INSTDIR\wx\lib\pubsub\core\weakmethod.py"
  Delete "$INSTDIR\wx\lib\pubsub\core\validatedefnargs.py"
  Delete "$INSTDIR\wx\lib\pubsub\core\treeconfig.py"
  Delete "$INSTDIR\wx\lib\pubsub\core\topicutils.py"
  Delete "$INSTDIR\wx\lib\pubsub\core\topictreetraverser.py"
  Delete "$INSTDIR\wx\lib\pubsub\core\topicobj.py"
  Delete "$INSTDIR\wx\lib\pubsub\core\topicmgr.py"
  Delete "$INSTDIR\wx\lib\pubsub\core\topicexc.py"
  Delete "$INSTDIR\wx\lib\pubsub\core\topicdefnprovider.py"
  Delete "$INSTDIR\wx\lib\pubsub\core\topicargspec.py"
  Delete "$INSTDIR\wx\lib\pubsub\core\publisherbase.py"
  Delete "$INSTDIR\wx\lib\pubsub\core\notificationmgr.py"
  Delete "$INSTDIR\wx\lib\pubsub\core\listenerbase.py"
  Delete "$INSTDIR\wx\lib\pubsub\core\listener.py"
  Delete "$INSTDIR\wx\lib\pubsub\core\kwargs\__init__.py"
  Delete "$INSTDIR\wx\lib\pubsub\core\kwargs\topicmgrimpl.py"
  Delete "$INSTDIR\wx\lib\pubsub\core\kwargs\topicargspecimpl.py"
  Delete "$INSTDIR\wx\lib\pubsub\core\kwargs\publishermixin.py"
  Delete "$INSTDIR\wx\lib\pubsub\core\kwargs\publisher.py"
  Delete "$INSTDIR\wx\lib\pubsub\core\kwargs\listenerimpl.py"
  Delete "$INSTDIR\wx\lib\pubsub\core\kwargs\datamsg.py"
  Delete "$INSTDIR\wx\lib\pubsub\core\itopicdefnprovider.py"
  Delete "$INSTDIR\wx\lib\pubsub\core\imp2.py"
  Delete "$INSTDIR\wx\lib\pubsub\core\callables.py"
  Delete "$INSTDIR\wx\lib\pubsub\core\arg1\__init__.py"
  Delete "$INSTDIR\wx\lib\pubsub\core\arg1\topicmgrimpl.py"
  Delete "$INSTDIR\wx\lib\pubsub\core\arg1\topicargspecimpl.py"
  Delete "$INSTDIR\wx\lib\pubsub\core\arg1\publishermixin.py"
  Delete "$INSTDIR\wx\lib\pubsub\core\arg1\publisher.py"
  Delete "$INSTDIR\wx\lib\pubsub\core\arg1\listenerimpl.py"
  Delete "$INSTDIR\VCRUNTIME140.dll"
  Delete "$INSTDIR\unicodedata.pyd"
  Delete "$INSTDIR\ucrtbase.dll"
  Delete "$INSTDIR\smartcard\scard\_scard.cp39-win_amd64.pyd"
  Delete "$INSTDIR\select.pyd"
  Delete "$INSTDIR\python39.dll"
  Delete "$INSTDIR\python3.dll"
  Delete "$INSTDIR\pyexpat.pyd"
  Delete "$INSTDIR\nft_display.py"
  Delete "$INSTDIR\NFT Card Manager.exe"
  Delete "$INSTDIR\multidict\_multidict.cp39-win_amd64.pyd"
  Delete "$INSTDIR\MSVCP140.dll"
  Delete "$INSTDIR\libssl-1_1.dll"
  Delete "$INSTDIR\libffi-7.dll"
  Delete "$INSTDIR\libcrypto-1_1.dll"
  Delete "$INSTDIR\frozenlist\_frozenlist.cp39-win_amd64.pyd"
  Delete "$INSTDIR\cryptography-36.0.2.dist-info\WHEEL"
  Delete "$INSTDIR\cryptography-36.0.2.dist-info\top_level.txt"
  Delete "$INSTDIR\cryptography-36.0.2.dist-info\RECORD"
  Delete "$INSTDIR\cryptography-36.0.2.dist-info\METADATA"
  Delete "$INSTDIR\cryptography-36.0.2.dist-info\LICENSE.PSF"
  Delete "$INSTDIR\cryptography-36.0.2.dist-info\LICENSE.BSD"
  Delete "$INSTDIR\cryptography-36.0.2.dist-info\LICENSE.APACHE"
  Delete "$INSTDIR\cryptography-36.0.2.dist-info\LICENSE"
  Delete "$INSTDIR\cryptography-36.0.2.dist-info\INSTALLER"
  Delete "$INSTDIR\cryptography\hazmat\bindings\_rust.pyd"
  Delete "$INSTDIR\cryptography\hazmat\bindings\_openssl.pyd"
  Delete "$INSTDIR\cryptnox_transparent.png"
  Delete "$INSTDIR\certifi\cacert.pem"
  Delete "$INSTDIR\base_library.zip"
  Delete "$INSTDIR\api-ms-win-crt-utility-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-crt-time-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-crt-string-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-crt-stdio-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-crt-runtime-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-crt-process-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-crt-multibyte-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-crt-math-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-crt-locale-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-crt-heap-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-crt-filesystem-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-crt-environment-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-crt-convert-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-crt-conio-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-core-util-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-core-timezone-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-core-sysinfo-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-core-synch-l1-2-0.dll"
  Delete "$INSTDIR\api-ms-win-core-synch-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-core-string-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-core-rtlsupport-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-core-profile-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-core-processthreads-l1-1-1.dll"
  Delete "$INSTDIR\api-ms-win-core-processthreads-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-core-processenvironment-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-core-namedpipe-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-core-memory-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-core-localization-l1-2-0.dll"
  Delete "$INSTDIR\api-ms-win-core-libraryloader-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-core-interlocked-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-core-heap-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-core-handle-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-core-file-l2-1-0.dll"
  Delete "$INSTDIR\api-ms-win-core-file-l1-2-0.dll"
  Delete "$INSTDIR\api-ms-win-core-file-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-core-errorhandling-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-core-debug-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-core-datetime-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-core-console-l1-1-0.dll"
  Delete "$INSTDIR\aiohttp\_websocket.cp39-win_amd64.pyd"
  Delete "$INSTDIR\aiohttp\_http_writer.cp39-win_amd64.pyd"
  Delete "$INSTDIR\aiohttp\_http_parser.cp39-win_amd64.pyd"
  Delete "$INSTDIR\aiohttp\_helpers.cp39-win_amd64.pyd"

  Delete "$SMPROGRAMS\NFT Card Manager\Uninstall.lnk"
  Delete "$DESKTOP\NFT Card Manager.lnk"
  Delete "$SMPROGRAMS\NFT Card Manager\NFT Card Manager.lnk"

  RMDir "$SMPROGRAMS\NFT Card Manager"
  RMDir "$INSTDIR\yarl"
  RMDir "$INSTDIR\wx\lib\pubsub\utils"
  RMDir "$INSTDIR\wx\lib\pubsub\core\kwargs"
  RMDir "$INSTDIR\wx\lib\pubsub\core\arg1"
  RMDir "$INSTDIR\wx\lib\pubsub\core"
  RMDir "$INSTDIR\wx\lib\pubsub"
  RMDir "$INSTDIR\wx"
  RMDir "$INSTDIR\smartcard\scard"
  RMDir "$INSTDIR\multidict"
  RMDir "$INSTDIR\frozenlist"
  RMDir "$INSTDIR\cryptography-36.0.2.dist-info"
  RMDir "$INSTDIR\cryptography\hazmat\bindings"
  RMDir "$INSTDIR\certifi"
  RMDir "$INSTDIR\aiohttp"
  RMDir "$INSTDIR"

  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  DeleteRegKey HKLM "${PRODUCT_DIR_REGKEY}"
  SetAutoClose true
SectionEnd