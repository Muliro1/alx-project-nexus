# Polling System - Entity Relationship Diagram

## Overview
This document describes the database schema for the Polling System, showing the relationships between entities and their attributes.

## Entities

### 1. User (Django's built-in User model)
**Primary Key:** `id` (AutoField)

**Attributes:**
- `username` (String, unique)
- `email` (String)
- `password` (String, hashed)
- `first_name` (String)
- `last_name` (String)
- `is_active` (Boolean)
- `date_joined` (DateTime)

### 2. Poll
**Primary Key:** `id` (AutoField)

**Attributes:**
- `question` (String, max_length=200)
- `created_at` (DateTime, auto_now_add=True)
- `expires_at` (DateTime)

**Business Rules:**
- A poll has an expiration date
- Polls are created with a timestamp

### 3. Option
**Primary Key:** `id` (AutoField)

**Attributes:**
- `poll_id` (ForeignKey to Poll)
- `text` (String, max_length=100)
- `votes` (Integer, default=0)

**Foreign Key Relationships:**
- `poll` → Poll (Many-to-One)

**Business Rules:**
- Each option belongs to exactly one poll
- Vote count is maintained as an integer field

### 4. Vote
**Primary Key:** `id` (AutoField)

**Attributes:**
- `option_id` (ForeignKey to Option)
- `voter_id` (ForeignKey to User, null=True)
- `voted_at` (DateTime, auto_now_add=True)

**Foreign Key Relationships:**
- `option` → Option (Many-to-One)
- `voter` → User (Many-to-One, nullable)

**Constraints:**
- Unique constraint on (`option`, `voter`) - prevents duplicate votes
- Index on (`voter`, `option`) for performance

**Business Rules:**
- A user can only vote once per option
- Votes are timestamped
- Voter can be null (anonymous voting)

## Relationships

### One-to-Many Relationships:
1. **Poll → Option**: One poll can have many options
2. **Option → Vote**: One option can have many votes
3. **User → Vote**: One user can have many votes

### Relationship Cardinalities:
- **Poll** (1) → **Option** (N): A poll must have at least one option
- **Option** (1) → **Vote** (N): An option can have zero or more votes
- **User** (1) → **Vote** (N): A user can vote on multiple options

## Database Constraints

### Primary Keys:
- All entities have auto-incrementing integer primary keys

### Foreign Keys:
- `Option.poll_id` → `Poll.id` (CASCADE delete)
- `Vote.option_id` → `Option.id` (CASCADE delete)
- `Vote.voter_id` → `User.id` (CASCADE delete, nullable)

### Unique Constraints:
- `Vote(option, voter)` - prevents duplicate votes per user per option

### Indexes:
- `Vote(voter, option)` - for efficient querying of user votes

## Business Logic

### Voting Rules:
1. Users can vote on multiple options across different polls
2. Users cannot vote twice on the same option
3. Votes are anonymous (voter can be null)
4. Polls have expiration dates
5. Vote counts are maintained as integer fields on the Option model

### Data Integrity:
1. When a poll is deleted, all its options are deleted (CASCADE)
2. When an option is deleted, all its votes are deleted (CASCADE)
3. When a user is deleted, all their votes are deleted (CASCADE)

## API Endpoints

The system provides REST API endpoints for:
- Creating and listing polls
- Creating options for polls
- Recording votes
- Viewing poll results
- User authentication and token generation 