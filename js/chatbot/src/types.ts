export interface MultimodalData {
	name: string;
	orig_name?: string;
	size?: number;
	data: string;
	user_message?: string;
	blob?: File;
	is_file?: boolean;
	mime_type?: string;
	alt_text?: string;
}