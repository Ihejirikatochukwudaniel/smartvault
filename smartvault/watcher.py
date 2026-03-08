"""Directory watching and event handling using watchdog."""

from __future__ import annotations

import time
from pathlib import Path
from threading import Timer
from typing import Any

from watchdog.events import FileSystemEventHandler, FileCreatedEvent
from watchdog.observers import Observer

from .organizer import FileOrganizer
from .logger import get_logger


class SmartVaultHandler(FileSystemEventHandler):
    """Handler that reacts to filesystem events for SmartVault."""

    def __init__(self, organizer: FileOrganizer) -> None:
        """Initialize with a reference to the organizer.

        Args:
            organizer: Instance of :class:`FileOrganizer` to delegate to.
        """
        self.organizer = organizer
        self._debounce_timers: dict[Path, Timer] = {}
        self.logger = get_logger(__name__)

    def on_created(self, event: FileCreatedEvent) -> None:  # type: ignore[override]
        """Handle new file creation events with debounce.

        Args:
            event: Filesystem event.
        """
        if event.is_directory:
            return
        path = Path(event.src_path)
        if path.name.startswith(".") or path.suffix.lower() in {".tmp", ".part"}:
            self.logger.debug("Ignoring hidden/temp file %s", path)
            return
        # debounce
        if path in self._debounce_timers:
            self._debounce_timers[path].cancel()
        timer = Timer(0.5, self._process, args=(path,))
        self._debounce_timers[path] = timer
        timer.start()

    def _process(self, path: Path) -> None:
        self.logger.info("Processing created file %s", path)
        self.organizer.organize_file(path)
        self._debounce_timers.pop(path, None)


class DirectoryWatcher:
    """Wrapper around watchdog observer for clean start/stop."""

    def __init__(self, watch_path: Path, organizer: FileOrganizer) -> None:
        """Store parameters and prepare observer.

        Args:
            watch_path: Directory to monitor.
            organizer: The organizer to use for events.
        """
        self.watch_path = watch_path
        self.organizer = organizer
        self.observer = Observer()
        self.logger = get_logger(__name__)

    def start(self) -> None:
        """Begin watching and block until interruption."""
        self.logger.info("Starting observer on %s", self.watch_path)
        handler = SmartVaultHandler(self.organizer)
        self.observer.schedule(handler, str(self.watch_path), recursive=False)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def stop(self) -> None:
        """Stop the observer gracefully."""
        self.logger.info("Stopping observer")
        self.observer.stop()
        self.observer.join()
