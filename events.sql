-- DROP SCHEMA public;

CREATE SCHEMA public AUTHORIZATION pg_database_owner;

-- DROP TYPE public."eventregistrationstatus";

CREATE TYPE public."eventregistrationstatus" AS ENUM (
	'PENDING',
	'ACCEPTED',
	'CANCELED');

-- DROP TYPE public."eventtype";

CREATE TYPE public."eventtype" AS ENUM (
	'VIRTUAL',
	'IN_PERSON',
	'HYBRID');

-- DROP TYPE public."sessionlevel";

CREATE TYPE public."sessionlevel" AS ENUM (
	'LEVEL_100',
	'LEVEL_200',
	'LEVEL_300',
	'LEVEL_400');

-- DROP TYPE public."sessionregistrationstatus";

CREATE TYPE public."sessionregistrationstatus" AS ENUM (
	'PENDING',
	'ACCEPTED',
	'CANCELED');

-- DROP TYPE public."sessionstatus";

CREATE TYPE public."sessionstatus" AS ENUM (
	'SUBMITTED',
	'APPROVED',
	'CANCELLED');

-- DROP TYPE public."sessiontype";

CREATE TYPE public."sessiontype" AS ENUM (
	'VIRTUAL',
	'IN_PERSON',
	'HYBRID');
-- public.address definition

-- Drop table

-- DROP TABLE public.address;

CREATE TABLE public.address (
	friendly_name varchar(255) NULL,
	description varchar(1000) NULL,
	street varchar(255) NOT NULL,
	apt_suite varchar(255) NULL,
	city varchar(100) NOT NULL,
	state varchar(100) NOT NULL,
	postal_code varchar(20) NOT NULL,
	country varchar(100) NOT NULL,
	id uuid NOT NULL,
	CONSTRAINT address_pkey PRIMARY KEY (id)
);


-- public.alembic_version definition

-- Drop table

-- DROP TABLE public.alembic_version;

CREATE TABLE public.alembic_version (
	version_num varchar(32) NOT NULL,
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);


-- public.organization definition

-- Drop table

-- DROP TABLE public.organization;

CREATE TABLE public.organization (
	id uuid NOT NULL,
	"name" varchar(255) NOT NULL,
	display_name varchar(255) NULL,
	short_description varchar(500) NOT NULL,
	profile_picture varchar NULL,
	profile_banner varchar NULL,
	contact_email varchar(255) NULL,
	linkedin_link varchar NULL,
	github_link varchar NULL,
	readme varchar NULL,
	slug varchar(255) NOT NULL,
	CONSTRAINT organization_pkey PRIMARY KEY (id),
	CONSTRAINT organization_slug_key UNIQUE (slug)
);


-- public."user" definition

-- Drop table

-- DROP TABLE public."user";

CREATE TABLE public."user" (
	email varchar(255) NOT NULL,
	is_active bool NOT NULL,
	is_superuser bool NOT NULL,
	full_name varchar(255) NULL,
	hashed_password varchar NOT NULL,
	id uuid NOT NULL,
	CONSTRAINT user_pkey PRIMARY KEY (id)
);
CREATE UNIQUE INDEX ix_user_email ON public."user" USING btree (email);


-- public."event" definition

-- Drop table

-- DROP TABLE public."event";

CREATE TABLE public."event" (
	"name" varchar(255) NOT NULL,
	short_description varchar(100) NULL,
	description varchar(255) NULL,
	start_time timestamp NOT NULL,
	end_time timestamp NOT NULL,
	event_type public."eventtype" NOT NULL,
	is_private bool NOT NULL,
	organization_name varchar(255) NULL,
	created_at timestamp NOT NULL,
	updated_at timestamp NOT NULL,
	id uuid NOT NULL,
	address_id uuid NULL,
	organization_id uuid NULL,
	slug varchar(255) NOT NULL,
	CONSTRAINT event_pkey PRIMARY KEY (id),
	CONSTRAINT event_slug_key UNIQUE (slug),
	CONSTRAINT event_address_id_fkey FOREIGN KEY (address_id) REFERENCES public.address(id),
	CONSTRAINT event_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organization(id)
);


-- public.eventdetails definition

-- Drop table

-- DROP TABLE public.eventdetails;

CREATE TABLE public.eventdetails (
	readme varchar NULL,
	code_of_conduct varchar NULL,
	sponsors varchar NULL,
	info_for_speakers varchar NULL,
	info_for_sponsors varchar NULL,
	info_for_staff varchar NULL,
	contact_info varchar NULL,
	resources varchar NULL,
	updated_at timestamp NOT NULL,
	id uuid NOT NULL,
	event_id uuid NOT NULL,
	CONSTRAINT eventdetails_event_id_key UNIQUE (event_id),
	CONSTRAINT eventdetails_pkey PRIMARY KEY (id),
	CONSTRAINT eventdetails_event_id_fkey FOREIGN KEY (event_id) REFERENCES public."event"(id)
);


-- public.eventorganizerlink definition

-- Drop table

-- DROP TABLE public.eventorganizerlink;

CREATE TABLE public.eventorganizerlink (
	event_id uuid NOT NULL,
	user_id uuid NOT NULL,
	CONSTRAINT eventorganizerlink_pkey PRIMARY KEY (event_id, user_id),
	CONSTRAINT eventorganizerlink_event_id_fkey FOREIGN KEY (event_id) REFERENCES public."event"(id),
	CONSTRAINT eventorganizerlink_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id)
);


-- public.eventregistration definition

-- Drop table

-- DROP TABLE public.eventregistration;

CREATE TABLE public.eventregistration (
	status public."eventregistrationstatus" NOT NULL,
	cancellation_reason varchar(500) NULL,
	is_speaker bool NOT NULL,
	is_organizer bool NOT NULL,
	is_sponsor bool NOT NULL,
	is_student bool NOT NULL,
	is_staff bool NOT NULL,
	created_at timestamp NOT NULL,
	updated_at timestamp NOT NULL,
	id uuid NOT NULL,
	event_id uuid NOT NULL,
	user_id uuid NOT NULL,
	CONSTRAINT eventregistration_pkey PRIMARY KEY (id),
	CONSTRAINT eventregistration_event_id_fkey FOREIGN KEY (event_id) REFERENCES public."event"(id),
	CONSTRAINT eventregistration_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id)
);


-- public.item definition

-- Drop table

-- DROP TABLE public.item;

CREATE TABLE public.item (
	description varchar(255) NULL,
	title varchar(255) NOT NULL,
	id uuid NOT NULL,
	owner_id uuid NOT NULL,
	CONSTRAINT item_pkey PRIMARY KEY (id),
	CONSTRAINT item_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public."user"(id) ON DELETE CASCADE
);


-- public.organizationadminlink definition

-- Drop table

-- DROP TABLE public.organizationadminlink;

CREATE TABLE public.organizationadminlink (
	organization_id uuid NOT NULL,
	user_id uuid NOT NULL,
	CONSTRAINT organizationadminlink_pkey PRIMARY KEY (organization_id, user_id),
	CONSTRAINT organizationadminlink_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organization(id),
	CONSTRAINT organizationadminlink_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id)
);


-- public.organizationmemberlink definition

-- Drop table

-- DROP TABLE public.organizationmemberlink;

CREATE TABLE public.organizationmemberlink (
	organization_id uuid NOT NULL,
	user_id uuid NOT NULL,
	CONSTRAINT organizationmemberlink_pkey PRIMARY KEY (organization_id, user_id),
	CONSTRAINT organizationmemberlink_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organization(id),
	CONSTRAINT organizationmemberlink_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id)
);


-- public."session" definition

-- Drop table

-- DROP TABLE public."session";

CREATE TABLE public."session" (
	title varchar(255) NOT NULL,
	short_description varchar(255) NULL,
	abstract varchar(500) NULL,
	start_time timestamp NOT NULL,
	end_time timestamp NOT NULL,
	status public."sessionstatus" NOT NULL,
	cancellation_reason varchar(500) NULL,
	tags _varchar NULL,
	"level" public."sessionlevel" NOT NULL,
	session_type public."sessiontype" NOT NULL,
	"location" varchar(255) NULL,
	slug varchar(255) NOT NULL,
	id uuid NOT NULL,
	event_id uuid NOT NULL,
	CONSTRAINT session_pkey PRIMARY KEY (id),
	CONSTRAINT session_slug_key UNIQUE (slug),
	CONSTRAINT session_event_id_fkey FOREIGN KEY (event_id) REFERENCES public."event"(id)
);


-- public.sessionregistration definition

-- Drop table

-- DROP TABLE public.sessionregistration;

CREATE TABLE public.sessionregistration (
	status public."sessionregistrationstatus" NOT NULL,
	cancelation_reason varchar(500) NULL,
	created_at timestamp NOT NULL,
	updated_at timestamp NOT NULL,
	id uuid NOT NULL,
	session_id uuid NOT NULL,
	user_id uuid NOT NULL,
	CONSTRAINT sessionregistration_pkey PRIMARY KEY (id),
	CONSTRAINT sessionregistration_session_id_fkey FOREIGN KEY (session_id) REFERENCES public."session"(id),
	CONSTRAINT sessionregistration_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id)
);


-- public.sessionreview definition

-- Drop table

-- DROP TABLE public.sessionreview;

CREATE TABLE public.sessionreview (
	title varchar(255) NOT NULL,
	body varchar(1000) NOT NULL,
	is_hidden bool NOT NULL,
	created_at timestamp NOT NULL,
	updated_at timestamp NOT NULL,
	id uuid NOT NULL,
	session_registration_id uuid NOT NULL,
	CONSTRAINT sessionreview_pkey PRIMARY KEY (id),
	CONSTRAINT sessionreview_session_registration_id_fkey FOREIGN KEY (session_registration_id) REFERENCES public.sessionregistration(id)
);


-- public.sessionspeakerlink definition

-- Drop table

-- DROP TABLE public.sessionspeakerlink;

CREATE TABLE public.sessionspeakerlink (
	session_id uuid NOT NULL,
	user_id uuid NOT NULL,
	CONSTRAINT sessionspeakerlink_pkey PRIMARY KEY (session_id, user_id),
	CONSTRAINT sessionspeakerlink_session_id_fkey FOREIGN KEY (session_id) REFERENCES public."session"(id),
	CONSTRAINT sessionspeakerlink_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id)
);


-- public.userprofile definition

-- Drop table

-- DROP TABLE public.userprofile;

CREATE TABLE public.userprofile (
	id uuid NOT NULL,
	user_id uuid NOT NULL,
	username varchar(50) NOT NULL,
	profile_picture varchar(255) NULL,
	headline varchar(255) NULL,
	bio varchar(1000) NULL,
	current_position varchar(255) NULL,
	current_company varchar(255) NULL,
	skills varchar(255) NULL,
	website varchar(255) NULL,
	linkedin varchar(255) NULL,
	github varchar(255) NULL,
	twitter varchar(255) NULL,
	work_experience varchar(255) NULL,
	education varchar(255) NULL,
	projects varchar(255) NULL,
	certifications varchar(255) NULL,
	CONSTRAINT userprofile_pkey PRIMARY KEY (id),
	CONSTRAINT userprofile_user_id_key UNIQUE (user_id),
	CONSTRAINT userprofile_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id)
);
CREATE UNIQUE INDEX ix_userprofile_username ON public.userprofile USING btree (username);



-- DROP FUNCTION public.uuid_generate_v1();

CREATE OR REPLACE FUNCTION public.uuid_generate_v1()
 RETURNS uuid
 LANGUAGE c
 PARALLEL SAFE STRICT
AS '$libdir/uuid-ossp', $function$uuid_generate_v1$function$
;

-- DROP FUNCTION public.uuid_generate_v1mc();

CREATE OR REPLACE FUNCTION public.uuid_generate_v1mc()
 RETURNS uuid
 LANGUAGE c
 PARALLEL SAFE STRICT
AS '$libdir/uuid-ossp', $function$uuid_generate_v1mc$function$
;

-- DROP FUNCTION public.uuid_generate_v3(uuid, text);

CREATE OR REPLACE FUNCTION public.uuid_generate_v3(namespace uuid, name text)
 RETURNS uuid
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/uuid-ossp', $function$uuid_generate_v3$function$
;

-- DROP FUNCTION public.uuid_generate_v4();

CREATE OR REPLACE FUNCTION public.uuid_generate_v4()
 RETURNS uuid
 LANGUAGE c
 PARALLEL SAFE STRICT
AS '$libdir/uuid-ossp', $function$uuid_generate_v4$function$
;

-- DROP FUNCTION public.uuid_generate_v5(uuid, text);

CREATE OR REPLACE FUNCTION public.uuid_generate_v5(namespace uuid, name text)
 RETURNS uuid
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/uuid-ossp', $function$uuid_generate_v5$function$
;

-- DROP FUNCTION public.uuid_nil();

CREATE OR REPLACE FUNCTION public.uuid_nil()
 RETURNS uuid
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/uuid-ossp', $function$uuid_nil$function$
;

-- DROP FUNCTION public.uuid_ns_dns();

CREATE OR REPLACE FUNCTION public.uuid_ns_dns()
 RETURNS uuid
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/uuid-ossp', $function$uuid_ns_dns$function$
;

-- DROP FUNCTION public.uuid_ns_oid();

CREATE OR REPLACE FUNCTION public.uuid_ns_oid()
 RETURNS uuid
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/uuid-ossp', $function$uuid_ns_oid$function$
;

-- DROP FUNCTION public.uuid_ns_url();

CREATE OR REPLACE FUNCTION public.uuid_ns_url()
 RETURNS uuid
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/uuid-ossp', $function$uuid_ns_url$function$
;

-- DROP FUNCTION public.uuid_ns_x500();

CREATE OR REPLACE FUNCTION public.uuid_ns_x500()
 RETURNS uuid
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/uuid-ossp', $function$uuid_ns_x500$function$
;