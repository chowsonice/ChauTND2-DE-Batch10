## Tìm structured dataset có 1,000,000 dòng; insert vào 1 hoặc nhiều tables. Thực hiện các câu query có cùng output với việc sử dụng where, group by, having khác nhau. Đo và so sánh thời gian chạy!

### Lý thuyết
#### Dataset: user_data

| user_id | member_type | money_spent |
| ------- | ----------- | ----------- |
| 1       | gold        | 40          |
| 2       | gold        | 5           |
| 3       | gold        | 23          |
| 4       | silver      | 19          |
| 5       | silver      | 5           |
| 6       | bronze      | 10          |
| 7       | bronze      | 5           |
| 8       | bronze      | 14          |
| 9       | bronze      | 8           |
| 10      | bronze      | 9           |
#### Query thực hiện:
##### Query sử dụng `WHERE`
```SQL
SELECT member_type, SUM(money_spent)
FROM user_data
GROUP BY member_type
WHERE NOT member_type = 'bronze'
```

Theo trình tự xử lý ta có
1. FROM: Lấy dữ liệu từ bảng `user_data` (10 dòng)
2. WHERE: filter lại tất cả các dòng có `member_type` là `bronze` (5 dòng)
3. GROUP BY: tổ chức lại, nhóm các dòng theo cột `member_type` (5 dòng)
4. SELECT: Chọn cột `member_type` và tiến hành tính tổng giá trị cột `money_spent` theo `member_type` (5 dòng)

Vậy ta thấy, do có filter ở bước `WHERE` được thực hiện từ sớm, số dòng DBMS phải xử lý giảm đáng kể
##### Query sử dụng `HAVING`
```SQL
SELECT member_type, SUM(money_spent)
FROM user_data
GROUP BY member_type
HAVING NOT member_type = 'bronze'
```

Theo trình tự xử lý ta có
1. FROM: Lấy dữ liệu từ bảng `user_data` (10 dòng)
2. GROUP BY: tổ chức lại, nhóm các dòng theo cột `member_type` (10 dòng)
3. HAVING: điều kiện sau khi GROUP BY, ta lọc hết tất cả các cột có `member_type` là `bronze` (5 dòng)
4. SELECT: Chọn cột `member_type` và tiến hành tính tổng giá trị cột `money_spent` theo `member_type` (5 dòng)

Vậy ta thấy, do không có filter `WHERE` nên `GROUP BY` phải xử lý nhiều bộ dữ liệu hơn
### Thực nghiệm trong PostgreSQL
#### Dataset used
- [AnimeList Dataset](https://www.kaggle.com/datasets/svanoo/myanimelist-dataset/data)
- Trong ví dụ này, ta có hai bảng, bảng `animelist_user` (1 123 284 dòng) và bảng `user_review` (9 951 550 dòng)
#### Query thực hiện:
##### Query sử dụng `HAVING`:
Query:
```SQL
discard plans;
explain analyze
select au.user_id, au.mean_score, count(*)
from animelist_user au
join user_review ur on au.user_id = ur.user_id
where au.mean_score > 9.5 
group by au.user_id 
```
Execution plan:
![](Images/Pasted%20image%2020240624142953.png)
![](Images/Pasted%20image%2020240624143103.png)
##### Query sử dụng `WHERE`:
Query:
```SQL
discard plans;
explain analyze
select au.user_id, au.mean_score, count(*)
from animelist_user au
join user_review ur on au.user_id = ur.user_id
group by au.user_id 
having au.mean_score > 9.5 
```
Execution plan:
![](Images/Pasted%20image%2020240624143227.png)
![](Images/Pasted%20image%2020240624143256.png)

#### Kết luận
Ta thấy rằng, tuy là điều kiện filter ở tận `HAVING`, nhưng PostgreSQL đã bắt đầu xử lý filter đó từ đầu, giống như đang sử dụng `WHERE` vậy. Ta thấy rằng PostgreSQL đã tự động tối ưu hoá câu truy vấn để xử lý rồi.