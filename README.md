# Task API
A simple API for managing tasks made in Django + DRF.

## Clone the Repository
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

## Additional Resources

### Insomnia API Collection

As a bonus for developers working on this project, we've included an Insomnia API Collection file named `[task_api_collection.json]` in this repository. This collection is designed to assist with API testing and development using the [Insomnia app](https://insomnia.rest/).

#### How to Use

1. **Download the Insomnia App:**
   If you haven't already, download and install the [Insomnia app](https://insomnia.rest/download/).

2. **Import the Collection:**
   Open Insomnia, go to `File -> Import` and select the `[task_api_collection.json]` file from this repository.

3. **Explore and Test:**
   You'll now have a set of pre-configured API requests ready for testing and development. Feel free to customize as needed.
