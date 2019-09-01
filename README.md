# ch-id-card-api
HTTP API for extract fields from chinese id cards

# example of request
```
http -f -S POST http://localhost:8000/get_the_same_img file@/path/input.jpg > ./out.jpg
http -f -S POST http://localhost:8000/get_square_img file@/path/input.jpg > ./out.jpg
http -f POST http://localhost:8000/card_exists file@/path/input.jpg
```
