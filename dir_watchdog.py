import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileMovedEvent, FileCreatedEvent, PatternMatchingEventHandler

observer = Observer()


class Handler(PatternMatchingEventHandler):
    def __init__(self, copy_to, *args, **kwargs):
        super(Handler, self).__init__(*args, **kwargs)
        self.copy_to = copy_to
        print('Start monitoring')

    def on_created(self, event: FileCreatedEvent):
        print('File Created: ', event.src_path)
        shutil.copy(event.src_path, self.copy_to)

    def on_moved(self, event: FileMovedEvent):
        print('File Moved: ', event.src_path)
        shutil.copy(event.src_path, self.copy_to)

copy_file_to = os.path.join("/home/mondorhino/Dropbox/Приложения", "Dropbox PocketBook/E-books/TomaChoice/")
observer.schedule(event_handler=Handler(copy_to=copy_file_to, patterns='*'), path='.')
observer.daemon = False
observer.start()
try:
    observer.join()
except KeyboardInterrupt:
    print('Stopped.')
    observer.stop()
    observer.join()
