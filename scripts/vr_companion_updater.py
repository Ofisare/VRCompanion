from ofisare import AutoUpdater

updater = AutoUpdater()
success, exception = updater.perform_update()
if success:
    updateLabel = "Update performed, stop and restart FreePIE"
else:
    updateLabel = str(exception)
        
diagnostics.watch(updateLabel)