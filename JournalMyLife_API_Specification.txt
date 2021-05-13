# API Specification:

### [POST] /api/register/
Request 
```json
{
	"username": <USER INPUT>,
	"password": <USER INPUT>
}
```
Response
```json
{
	"session_token": <GENERATED SESSION TOKEN>,
	"session_expiration": <GENERATED SESSION EXPIRATION TIME>,
	"update_token": <GENERATED UPDATE TOKEN>
}
```

### [POST] /api/login/
Request 
```json
{
	"username": <USER INPUT>,
	"password": <USER INPUT>
}
```
Response
```json
{
	"session_token": <GENERATED SESSION TOKEN>,
	"session_expiration": <GENERATED SESSION EXPIRATION TIME>,
	"update_token": <GENERATED UPDATE TOKEN>
}
```

### [POST] /session/
Response
```json
{
	"session_token": <GENERATED SESSION TOKEN>,
	"session_expiration": <GENERATED SESSION EXPIRATION TIME>,
	"update_token": <GENERATED UPDATE TOKEN>
}
```

[GET] /api/login/posts/
Response
```json
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
Response
```json
{
	"success": true,
	"data": <POST WITH DATE {year}/{month}/{day}>
}
```

### [POST] /api/login/posts/
Request
```json
{
	"year": <USER INPUT>,
	"month": <USER INPUT>,
	"day": <USER INPUT>,
	"location": <USER INPUT>,
	"entry": <USER INPUT>

}
```
Reponse
```json
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
Reponse
```json
{
	"success": true,
	"data": <DELETED POST>
}
```

### [POST] /api/login/posts/{post_id}/
Request
```json
{
	"entry": <USER INPUT>,
	"location": <USER INPUT>
}
```

Response
```json
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
Request
```json
{
	"image_data": <USER INPUT IN BASE64>
}
```
Reponse
```json
{
	"success": true,
	"data": {
			"id": <ID>,
			"url": <GENERATED IMAGE URL>,
			"created_at": <GENERATED CREATION TIME>,
		}
}
```


			
