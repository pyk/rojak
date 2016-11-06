-- Usage:
--      call get_constraints('rojak_test_5', 'sentiment');
-- Check:
--      SELECT * FROM mysql.proc WHERE name='get_constraints' \G;
DROP PROCEDURE IF EXISTS get_constraints;
DELIMITER //
    CREATE PROCEDURE 
        get_constraints(in_db_name VARCHAR(255), in_table_name VARCHAR(255))
    BEGIN
        SELECT 
            TABLE_SCHEMA,
            TABLE_NAME,
            COLUMN_NAME,
            CONSTRAINT_NAME,
            REFERENCED_TABLE_NAME,
            REFERENCED_COLUMN_NAME
        FROM information_schema.KEY_COLUMN_USAGE
        WHERE TABLE_SCHEMA=in_db_name AND TABLE_NAME=in_table_name;
    END //
DELIMITER ;
