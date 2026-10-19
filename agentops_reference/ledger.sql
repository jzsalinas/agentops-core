-- PROPOSED durable MVP storage. Not a running service. Payloads are minimized.
PRAGMA foreign_keys=ON;
CREATE TABLE events (
 project_id TEXT NOT NULL, event_id TEXT NOT NULL, digest TEXT NOT NULL,
 source_object_id TEXT NOT NULL, observed_revision TEXT NOT NULL,
 PRIMARY KEY(project_id,event_id)
);
CREATE TABLE deliveries (
 project_id TEXT NOT NULL, adapter TEXT NOT NULL, delivery_id TEXT NOT NULL,
 event_id TEXT NOT NULL, digest TEXT NOT NULL,
 PRIMARY KEY(project_id,adapter,delivery_id),
 FOREIGN KEY(project_id,event_id) REFERENCES events(project_id,event_id)
);
CREATE TABLE tasks (
 project_id TEXT NOT NULL, task_id TEXT NOT NULL, task_revision INTEGER NOT NULL,
 business_key TEXT NOT NULL, record_revision INTEGER NOT NULL DEFAULT 1,
 status_json TEXT NOT NULL, PRIMARY KEY(project_id,task_id,task_revision),
 UNIQUE(project_id,business_key)
);
CREATE TABLE claims (
 project_id TEXT NOT NULL, business_key TEXT NOT NULL, execution_id TEXT NOT NULL,
 owner_id TEXT NOT NULL, lease_expires_at TEXT NOT NULL, fencing_token INTEGER NOT NULL,
 PRIMARY KEY(project_id,business_key), CHECK(fencing_token>0)
);
CREATE TABLE authorizations (
 project_id TEXT NOT NULL, authorization_id TEXT NOT NULL, max_uses INTEGER NOT NULL,
 used_count INTEGER NOT NULL DEFAULT 0, record_json TEXT NOT NULL,
 PRIMARY KEY(project_id,authorization_id), CHECK(used_count>=0 AND used_count<=max_uses)
);
CREATE TABLE attempts (
 project_id TEXT NOT NULL, execution_id TEXT NOT NULL, attempt_number INTEGER NOT NULL,
 attempt_id TEXT NOT NULL, fencing_token INTEGER NOT NULL, record_json TEXT NOT NULL,
 PRIMARY KEY(project_id,attempt_id), UNIQUE(project_id,execution_id,attempt_number)
);
CREATE TABLE outbox (
 project_id TEXT NOT NULL, effect_key TEXT NOT NULL, target_ref TEXT NOT NULL,
 body_digest TEXT NOT NULL, marker TEXT NOT NULL, status TEXT NOT NULL,
 remote_ref TEXT, send_count INTEGER NOT NULL DEFAULT 0,
 PRIMARY KEY(project_id,effect_key), UNIQUE(project_id,marker),
 CHECK(status IN ('PENDING','SENDING','CONFIRMED','UNKNOWN','FAILED'))
);
CREATE TABLE audit (
 sequence INTEGER PRIMARY KEY, project_id TEXT NOT NULL, record_ref TEXT NOT NULL,
 digest TEXT NOT NULL, previous_digest TEXT, occurred_at TEXT NOT NULL
);
-- Application MUST compare stored digest on every uniqueness conflict, not ignore it.
-- Claim/attempt/authorization reservation/outbox creation use BEGIN IMMEDIATE + CAS.
-- Expired claims require reconciliation, then increment fencing_token atomically.
-- SQLite uniqueness does NOT establish exactly-once effects at GitHub.
