@echo off
echo Closing running instances of Google Chrome...
taskkill /f /im chrome.exe 2>nul

echo Launching Google Chrome in isolated POS mode with silent printing...
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --kiosk-printing --user-data-dir="C:\POS_Chrome_Profile" "http://127.0.0.1:8000/Products/Pos"

exit
