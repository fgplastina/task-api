## Clone the repo 
```bash
git clone https://github.com/fgplastina/task-api/
```

 
## Setting up the project
###### Build and run the application, it will be deployed at http://localhost:8000/api/
```bash
make run
```


###### Run migrations
```bash
make migrate
```
###### Load fixture
```bash
make loaddata
```
## Testing the app
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
