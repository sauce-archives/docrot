import os


class FileOutputWrapper(object):
    """
    Wraps a subclass of formatter.FormatterBase to direct output from blobs
    to individual files rather than stdout.
    """

    def __init__(self, formatter, file_ext, output_dir):
        self.formatter = formatter
        self.file_ext = file_ext

        # Setup output directory
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        self.output_dir = output_dir

    def _get_output_filename(self, blob):
        return os.path.join(self.output_dir, "{}.{}".format(
            blob.name, self.file_ext))

    def format(self):
        blobs = self.formatter.blobs
        for blob in blobs:
            with open(self._get_output_filename(blob), 'wb') as f:
                self.formatter.blobs = [blob]
                self.formatter.update_stream(f)
                self.formatter.format()
