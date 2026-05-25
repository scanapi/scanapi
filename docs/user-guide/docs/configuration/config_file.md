# Configuration File

If you want to configure the ScanAPI with a file, you can create a local `scanapi.conf` file where you are running the ScanAPI CLI or a global `scanapi.conf` file following the XDG Base Directory Specification.

```yaml
project_name: DemoAPI # This will be rendered in the Report Title.
spec_path: my_path/scanapi.yaml # API specification file path
output_path: my_path/my-report.html # Report output path.
template: my_template.jinja # Custom report template path.
```
