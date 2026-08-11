function AttachmentList({ documents, images, removeDocument, removeImage }) {
    return (
        <div>
            {documents.map((doc) => (
                <span key = {doc.file_uuid}>
                    {doc.filename}
                    <button onClick={() => removeDocument(doc.file_uuid)}>X</button>
                </span>
            ))}
            {images.map((img) => (
                <span key = {img.id}>
                    {img.filename}
                    <button onClick={() => removeImage(img.id)}>X</button>
                </span>
            ))}
        </div>
    );
}

export default AttachmentList