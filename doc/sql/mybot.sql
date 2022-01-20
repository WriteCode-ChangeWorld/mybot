CREATE DATABASE IF NOT EXISTS mybot DEFAULT CHARSET utf8mb4;
-- user表
CREATE TABLE users(
  id int AUTO_INCREMENT PRIMARY KEY,
  uid VARCHAR(20) NOT NULL,
  gid VARCHAR(20) NOT NULL,
  user_level INT(5) NOT NULL,
	user_limit_cycle  INT(3) NOT NULL,
	user_limit_count  INT(3) NOT NULL,
	user_call_count  INT(3 ) NOT NULL,
  magic_thing INT(8) NOT NULL,
	is_qqBlocked TINYINT(1) NOT NULL,
  create_date DATETIME NOT NULL,
  last_call_date DATETIME NOT NULL,
  cycle_expiration_time DATETIME NOT NULL
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- group_chats表
CREATE TABLE group_chats(
  id int AUTO_INCREMENT PRIMARY KEY,
  gid VARCHAR(20) NOT NULL,
  group_name VARCHAR(100) NOT NULL,
  group_level  INT(5) NOT NULL,
  is_qqBlocked TINYINT(1) NOT NULL
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- messages表
CREATE TABLE messages(
  id int AUTO_INCREMENT PRIMARY KEY,
  message_type VARCHAR(20) NOT NULL,
  user_id VARCHAR(20) NOT NULL,
  user_name VARCHAR(100) NOT NULL,
  group_id VARCHAR(20) NOT NULL,
  group_name VARCHAR(100) NOT NULL,
  raw_message VARCHAR(1024) NOT NULL,
	message_datetime DATETIME NOT NULL
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- plugin_info表
CREATE TABLE plugin_info(
  id int AUTO_INCREMENT PRIMARY KEY,
  plugin_name VARCHAR(40) NOT NULL,
  plugin_type INT(3) NOT NULL,
  plugin_level INT(5) NOT NULL,
  plugin_status INT(3) NOT NULL
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- tasks表
CREATE TABLE tasks(
  id int AUTO_INCREMENT PRIMARY KEY,
  creator_id VARCHAR(20) NOT NULL,
  group_id VARCHAR(20) NOT NULL,
  task_type VARCHAR(30) NOT NULL,
  by_plugin VARCHAR(30) NOT NULL,
  create_time DATETIME NOT NULL,
  task_status VARCHAR(20) NOT NULL,
  task_level INT(5) NOT NULL,
  exec_task VARCHAR(1024) NOT NULL,
  exec_time DATETIME NOT NULL,
  report_user_id VARCHAR(20) NOT NULL,
  report_group_id VARCHAR(20) NOT NULL
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;


SELECT @@sql_mode;