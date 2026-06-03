@echo off
echo Closing running instances of Microsoft Edge...
taskkill /f /im msedge.exe 2>nul

echo Launching Microsoft Edge in isolated POS mode with silent printing...
start "" "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --kiosk-printing --user-data-dir="C:\POS_Edge_Profile" "http://127.0.0.1:8000/Products/Pos"

exit
