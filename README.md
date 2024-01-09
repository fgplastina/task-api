## Clone the repo 
```bash
git clone https://github.com/fgplastina/<app>/
```
### Build and run the application, it will be at http://localhost:8000/api/
```bash
make run
```

## Setting up the project
###### Run migrations
```bash
make migrate
```
###### Load fixture
```bash
make loaddata
```
## Setting up the project
###### Run all tests
```bash
make tests args=core.tests
```
###### Run tests for models
```bash
make tests args=core.tests.models
```
###### Run tests for viewsets 
```bash
make tests args=core.tests.viewsets_tests
```
