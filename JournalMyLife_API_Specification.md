# API Specification:

### [POST] /api/register/
- Register an account
Request 
```
{
	"username": <USER INPUT>,
	"password": <USER INPUT>
}
```
Response
```
{
	"session_token": <GENERATED SESSION TOKEN>,
	"session_expiration": <GENERATED SESSION EXPIRATION TIME>,
	"update_token": <GENERATED UPDATE TOKEN>
}
```

### [POST] /api/login/
- Login to account
Request 
```
{
	"username": <USER INPUT>,
	"password": <USER INPUT>
}
```
Response
```
{
	"session_token": <GENERATED SESSION TOKEN>,
	"session_expiration": <GENERATED SESSION EXPIRATION TIME>,
	"update_token": <GENERATED UPDATE TOKEN>
}
```

### [POST] /session/
- Updates session
Response
```
{
	"session_token": <GENERATED SESSION TOKEN>,
	"session_expiration": <GENERATED SESSION EXPIRATION TIME>,
	"update_token": <GENERATED UPDATE TOKEN>
}
```

### [GET] /api/login/posts/
- Returns all posts
Response
```
{
	"success": true,
	"data": [
		{
			"id": 1,
			"year": 2021,
			"month": 5,
			"day": 14,
			"location": "Ithaca, NY",
			"entry": "Today was fun",
			"user_id": <USER ID>
			"images": [<SERIALIZED IMAGES>, ...]
		},
		...
		]
}
```

### [GET] /api/login/posts/{year}/{month}/{day}/
- Returns posts on a specificed date
Response
```
{
	"success": true,
	"data": <POST WITH DATE {year}/{month}/{day}>
}
```

### [POST] /api/login/posts/
- Creates a post
Request
```
{
	"year": <USER INPUT>,
	"month": <USER INPUT>,
	"day": <USER INPUT>,
	"location": <USER INPUT>,
	"entry": <USER INPUT>

}
```
Response
```
{
	"success": true,
	"data": {
			"id": <ID>,
			"year": <USER INPUT FOR YEAR>,
			"month": <USER INPUT FOR MONTH>,
			"day": <USER INPUT FOR DAY>,
			"location": <USER INPUT FOR LOCATION>,
			"entry": <USER INPUT FOR ENTRY>,
			"user_id": <USER ID>
			"images": []
		}
}
	
```
		
### [DELETE] /api/login/posts/{post_id}/
- Deletes a post with specified ID
Response
```
{
	"success": true,
	"data": <DELETED POST>
}
```

### [POST] /api/login/posts/{post_id}/
- Updates a post with a specified ID
Request
```
{
	"entry": <USER INPUT>,
	"location": <USER INPUT>
}
```

Response
```
{
	"success": true,
	"data": {
			"id": 1,
			"year": 2021,
			"month": 5,
			"day": 14,
			"location": <USER INPUT FOR LOCATION>,
			"entry": <USER INPUT FOR ENTRY>,
			"user_id": <USER ID>
			"images": [<SERIALIZED IMAGES>, ...]
		}
}
```

### [POST] /api/login/posts/{post_id}/upload/
- Uploads a picture to a post with a specified ID
Request
```
{
	"image_data": <USER INPUT IN BASE64>
}
```
Response
```
{
	"success": true,
	"data": {
			"id": <ID>,
			"url": <GENERATED IMAGE URL>,
			"created_at": <GENERATED CREATION TIME>,
		}
}
```


			
