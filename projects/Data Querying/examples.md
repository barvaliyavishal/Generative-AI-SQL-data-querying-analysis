# Examples — sample questions, SQL, and expected outputs

This file contains example natural-language questions, the SQL the app should generate (or a safe equivalent), and the expected results given the seeded `example.db` in this repo.

Note: the sample DB contains three customers and five sales rows seeded by `create_example_db.py`.

## 1) Which customers spent the most in March?

- Example SQL:

```sql
SELECT c.name, SUM(s.amount) AS total_spent
FROM customer c
JOIN sales s ON c.customer_id = s.customer_id
WHERE sale_date BETWEEN '2023-03-01' AND '2023-03-31'
GROUP BY c.customer_id, c.name
ORDER BY total_spent DESC;
```

- Expected result (based on seeded data):

```json
[ ["Asha Sharma", 1225.0], ["Rahul Verma", 300.0] ]
```

## 2) Show total sales by product

- Example SQL:

```sql
SELECT product, SUM(amount) AS total_sales
FROM sales
GROUP BY product
ORDER BY total_sales DESC;
```

- Expected result:

```json
[ ["Laptop", 2300.0], ["Monitor", 300.0], ["Keyboard", 45.0], ["Mouse", 25.0] ]
```

## 3) List customers

- Example SQL:

```sql
SELECT customer_id, name, email
FROM customer
ORDER BY customer_id;
```

- Expected result:

```json
[ [1, "Asha Sharma", "asha@example.com"], [2, "Rahul Verma", "rahul@example.com"], [3, "Priya Singh", "priya@example.com"] ]
```

## 4) Sales in May 2023

- Example SQL:

```sql
SELECT * FROM sales WHERE sale_date BETWEEN '2023-05-01' AND '2023-05-31';
```

- Expected result:

```json
[ [5, 2, "Laptop", 1100.0, "2023-05-20"] ]
```

If you want, I can add a short test script that executes these queries against `example.db` and asserts the expected outputs.
