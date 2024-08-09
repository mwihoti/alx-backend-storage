-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser that computes and store the average weighted score for a student.

DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser(user_id INT)
BEGIN
    DECLARE total_weight_score FLOAT DEFAULT 0;
    DECLARE total_weight FLOAT DEFAULT 0;

    SELECT SUM(corrections.score * projects.weight)
        INTO total_weight_score
        FROM corrections
            INNER JOIN projects
                ON corrections.project_id = projects.id
        WHERE corrections.user_id = user_id;
    
    SELECT SUM(projects.weight)
        INTO total_weight
        FROM corrections
            INNER JOIN projects
                ON corrections.project_id = projects.id
        WHERE corrections.user_id = user_id;
    
    IF total_weight = 0 THEN
        UPDATE users
            SET average_score = 0
            WHERE id = user_id;
    ELSE
        UPDATE users
        SET users.average_score = total_weight_score / total_weight
        WHERE id = user_id;
    END IF;
END $$
DELIMITER ;
