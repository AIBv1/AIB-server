CREATE TABLE meal_record (
                             meal_id INT AUTO_INCREMENT PRIMARY KEY,
                             user_id INT,
                             meal_time DATETIME,
                             calories DECIMAL(5,2) NOT NULL,
                             protein DECIMAL(5,2) NOT NULL,
                             fat DECIMAL(5,2) NOT NULL,
                             carbs DECIMAL(5,2) NOT NULL,
                             description VARCHAR(255),
                             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                             FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE
);

CREATE TABLE meal_records (
                              id INT AUTO_INCREMENT PRIMARY KEY,
                              user_id INT,
                              meal_date DATE, -- 새로 추가된 필드
                              meal_time DATETIME,
                              meal_type ENUM('breakfast', 'lunch', 'dinner', 'snack', 'late_night') NOT NULL, -- 끼니 종류를 나타내는 ENUM 필드 추가
                              calories DECIMAL(5,2) NOT NULL,
                              protein DECIMAL(5,2) NOT NULL,
                              fat DECIMAL(5,2) NOT NULL,
                              carbs DECIMAL(5,2) NOT NULL,
                              description VARCHAR(255),
                              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                              updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                              FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
