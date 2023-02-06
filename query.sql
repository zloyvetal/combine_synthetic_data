SELECT ac.acc_id AS account_id,
       ac.company_name AS company_name,
       COALESCE(refr.recency_score, 0) AS recency_score,
       COALESCE(refr.frequency_score, 0) AS frequency_score,
       COALESCE(mo.monetary_score, 0) AS monetary_score,
       sc.segment_label AS segment_label
FROM accounts ac
LEFT JOIN (SELECT MAX(closing_date) AS last_win_date,
                  CASE
                     WHEN EXTRACT(month from AGE(NOW(), MAX(closing_date))) < 6 THEN 5
                     WHEN EXTRACT(month from AGE(NOW(), MAX(closing_date))) < 12 THEN 4
                     WHEN EXTRACT(month from AGE(NOW(), MAX(closing_date))) < 18 THEN 3
                     WHEN EXTRACT(month from AGE(NOW(), MAX(closing_date))) < 24 THEN 2
                  ELSE 1
                  END recency_score,
                  COUNT(*) AS won_count,
                  CASE
                     WHEN COUNT(*) > 60 THEN 5
                     WHEN COUNT(*) > 30 THEN 4
                     WHEN COUNT(*) > 10 THEN 3
                     WHEN COUNT(*) > 3 THEN 2
                  ELSE 1
                  END frequency_score,
                  account_id
           FROM opportunities
           WHERE stage = 'Won'
           GROUP BY account_id
) refr ON ac.acc_id = refr.account_id
LEFT JOIN (SELECT SUM(re.value) AS revenue,
                  CASE
                     WHEN SUM(re.value) > 3000000 THEN 5
                     WHEN SUM(re.value) > 1000000 THEN 4
                     WHEN SUM(re.value) > 300000 THEN 3
                     WHEN SUM(re.value) > 100000 THEN 2
                  ELSE 1
                  END monetary_score,
                  op.account_id AS account_id
           FROM revenue re
           LEFT JOIN opportunities op ON re.opportunity_id = op.opportunity_id
           GROUP BY op.account_id
) mo ON ac.acc_id = mo.account_id
LEFT JOIN segment_codes sc ON COALESCE(refr.recency_score, 0) = sc.recency_score AND
                              COALESCE(refr.frequency_score, 0) = sc.frequency_score AND
                              COALESCE(mo.monetary_score, 0) = sc.monetary_score
ORDER BY ac.acc_id