# Lab Guide Structure
## What is the lab and Architecture
## Generate a Provider JSON
- Update the CSV
- Run the `onug_csnf_mapping_load.py -i CSV_file -o output_json.json`
- upload the JSON to somewhere public or use the one in here

## Install FN
- https://fnproject.io/tutorials/install/

## Deploy Function
- create app ex. onugfall
- cd to finding-to-csnf-function
- fn deploy to app `fn deploy --app onugfall --local`

## Use it
- fn invoke 
- VIA Rest API
    - get invocation endpoint
    - Use Postman collection and one of the sample findings uploaded