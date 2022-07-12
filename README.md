# napari-matous
Tools I build during my time at the Francis Crick Institute

----------------------------------

## Installation

To install `napari-matous` it is recommended to create a fresh `conda` environment with Python 3.9:
```
conda create -n matous_env python=3.9
```

Then activate the `conda`:
```
conda activate matous_env
```
Next install the following essential packages using `conda`:
```
conda install -c anaconda pyqt grpcio
```
After, install `napari` with this command via [pip]:
```
pip install "napari[all]"
```
Lastly you can install `napari-matous` via [pip]:

    pip install git+https://github.com/m-elphick/napari-matous.git


## Contributing

Contributions are very welcome. Tests can be run with [tox], please ensure
the coverage at least stays the same before you submit a pull request.

## License

Distributed under the terms of the [MIT] license,
"napari-matous" is free and open source software

## Issues

If you encounter any problems, please [file an issue] along with a detailed description.

[napari]: https://github.com/napari/napari
[Cookiecutter]: https://github.com/audreyr/cookiecutter
[@napari]: https://github.com/napari
[MIT]: http://opensource.org/licenses/MIT
[BSD-3]: http://opensource.org/licenses/BSD-3-Clause
[GNU GPL v3.0]: http://www.gnu.org/licenses/gpl-3.0.txt
[GNU LGPL v3.0]: http://www.gnu.org/licenses/lgpl-3.0.txt
[Apache Software License 2.0]: http://www.apache.org/licenses/LICENSE-2.0
[Mozilla Public License 2.0]: https://www.mozilla.org/media/MPL/2.0/index.txt
[cookiecutter-napari-plugin]: https://github.com/napari/cookiecutter-napari-plugin

[file an issue]: https://github.com/m-elphick/napari-matous/issues

[napari]: https://github.com/napari/napari
[tox]: https://tox.readthedocs.io/en/latest/
[pip]: https://pypi.org/project/pip/
[PyPI]: https://pypi.org/
