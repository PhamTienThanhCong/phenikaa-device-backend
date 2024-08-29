Table "cameras" {
  "id" int(11) [pk, not null]
  "name" varchar(255) [default: NULL]
  "location_code" varchar(255) [default: NULL]
  "location" varchar(255) [default: NULL]
  "status" int(11) [default: NULL]
  "stream_url" varchar(255) [default: NULL]
}

Table "customers" {
  "id" int(11) [pk, not null]
  "role" int(11) [default: NULL]
  "email" varchar(100) [default: NULL]
  "full_name" varchar(100) [default: NULL]
  "avatar" varchar(250) [default: NULL]
  "birth_date" varchar(20) [default: NULL]
  "gender" int(11) [default: NULL]
  "address" varchar(100) [default: NULL]
  "phone_number" varchar(20) [default: NULL]
  "card_id" varchar(20) [default: NULL]
  "date_start" varchar(20) [default: NULL]
  "expired" tinyint(1) [default: NULL]
  "department" varchar(100) [default: NULL]
  "status" int(11) [default: NULL]
}

Table "devices" {
  "id" int(11) [pk, not null]
  "name" varchar(100) [ref: > device_category.name, default: NULL]
  "category" varchar(100) [default: NULL]
  "image" varchar(255) [default: NULL]
  "presigned_url" varchar(255) [default: NULL]
  "information" varchar(255) [default: NULL]
  "note" varchar(255) [default: NULL]
  "total" int(11) [default: NULL]
  "total_used" int(11) [default: NULL]
  "total_maintenance" int(11) [default: NULL]
  "is_active" tinyint(1) [default: NULL]
}

Table "device_borrowing" {
  "id" int(11) [pk, not null]
  "name" varchar(100) [default: NULL]
  "is_returned" tinyint(1) [default: NULL]
  "devices" longtext [ref: <> devices.id, default: NULL]
  "user_id" int(11) [ref: > users.id, default: NULL]
  "customer_id" int(11) [ref: > customers.id, default: NULL]
  "returning_date" datetime [default: NULL]
  "retired_date" datetime [default: NULL]
  "note" varchar(255) [default: NULL]
  "created_at" datetime [default: NULL]
}

Table "device_category" {
  "id" int(11) [pk, not null]
  "name" varchar(100) [default: NULL]
  "is_active" tinyint(1) [default: NULL]
  "image" varchar(255) [default: NULL]
  "presigned_url" varchar(255) [default: NULL]
}

Table "device_repairs" {
  "id" int(11) [pk, not null]
  "name" varchar(100) [default: NULL]
  "is_returned" tinyint(1) [default: NULL]
  "devices" longtext [ref: <> devices.id, default: NULL]
  "user_id" int(11) [ref: > users.id, default: NULL]
  "service_id" int(11) [ref: > maintenance_services.id, default: NULL]
  "returning_date" datetime [default: NULL]
  "retired_date" datetime [default: NULL]
  "note" varchar(255) [default: NULL]
  "created_at" datetime [default: NULL]
}

Table "maintenance_services" {
  "id" int(11) [pk, not null]
  "guardian" varchar(100) [not null]
  "name" varchar(100) [not null]
  "description" varchar(255) [default: NULL]
  "address" varchar(255) [default: NULL]
  "phone" varchar(20) [not null]
  "email" varchar(100) [not null]
  "status" tinyint(1) [default: NULL]
  "map_url" varchar(255) [default: NULL]
}

Table "notifies" {
  "id" int(11) [pk, not null]
  "customer_id" int(11) [ref: > customers.id, default: NULL]
  "title" varchar(255) [default: NULL]
  "category" varchar(255) [default: NULL]
  "content" varchar(255) [default: NULL]
  "explain" varchar(255) [default: NULL]
  "is_read" tinyint(1) [default: NULL]
  "is_cancel" tinyint(1) [default: NULL]
  "created_at" datetime [default: NULL]
  "confirmed_at" datetime [default: NULL]
  "user_id" int(11) [ref: > users.id, default: NULL]
  "location_info" longtext [default: NULL]
}

Table "profiles" {
  "id" int(11) [pk, not null]
  "user_id" int(11) [ref: > users.id, default: NULL]
  "full_name" varchar(100) [default: NULL]
  "avatar" varchar(100) [default: NULL]
  "birth_date" varchar(20) [default: NULL]
  "gender" int(11) [default: NULL]
  "address" varchar(100) [default: NULL]
  "phone_number" varchar(20) [default: NULL]
  "card_id" varchar(20) [default: NULL]
}

Table "rooms" {
  "room_id" varchar(30) [pk, not null]
  "category" varchar(100) [default: NULL]
  "house_name" varchar(20) [default: NULL]
  "manager" varchar(100) [default: NULL]
  "detail" longtext [default: NULL]
  "note" varchar(255) [default: NULL]
  "is_active" tinyint(1) [default: NULL]
  "is_using" tinyint(1) [default: NULL]
  "is_maintenance" tinyint(1) [default: NULL]
}

Table "room_bookings" {
  "id" int(11) [pk, not null]
  "name" varchar(100) [default: NULL]
  "room_id" varchar(30) [ref: > rooms.room_id, default: NULL]
  "user_id" int(11) [ref: > users.id, default: NULL]
  "customer_id" int(11) [ref: > customers.id, default: NULL]
  "total_customer" int(11) [default: NULL]
  "date_booking" date [default: NULL]
  "start_time" time [default: NULL]
  "end_time" time [default: NULL]
  "note" varchar(255) [default: NULL]
  "created_at" datetime [default: NULL]
  "updated_at" datetime [default: NULL]
  "is_active" tinyint(1) [default: NULL]
}

Table "users" {
  "id" int(11) [pk, not null]
  "full_name" varchar(50) [default: NULL]
  "email" varchar(50) [default: NULL]
  "password" varchar(250) [default: NULL]
  "role" int(11) [default: NULL]
  "is_active" int(11) [default: NULL]
}
