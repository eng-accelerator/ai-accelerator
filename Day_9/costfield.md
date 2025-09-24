# Cost
## Tiering
start_token
end_token

## Input
input_text_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(38, 24), nullable=True)
input_text_cached_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(38, 24), nullable=True)
input_text_cache_write_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(38, 24), nullable=True)
input_text_batch_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(38, 24), nullable=True)



input_image_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(38, 24), nullable=True)
input_image_cached_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(38, 24), nullable=True)
input_image_cache_write_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(38, 24), nullable=True)
input_image_batch_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(38, 24), nullable=True)


input_audio_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(38, 24), nullable=True)
input_audio_cached_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(38, 24), nullable=True)
input_audio_cache_write_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(38, 24), nullable=True)
input_audio_batch_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(38, 24), nullable=True)

## Per-minute cache storage (input only)
input_cached_text_price_per_min: Mapped[Optional[Decimal]] = mapped_column(Numeric(38, 24), nullable=True)
input_cached_image_price_per_min: Mapped[Optional[Decimal]] = mapped_column(Numeric(38, 24), nullable=True)
input_cached_audio_price_per_min: Mapped[Optional[Decimal]] = mapped_column(Numeric(38, 24), nullable=True)

## OUTPUT (base+batch)
output_text_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(38, 24), nullable=True)
output_text_batch_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(38, 24), nullable=True)
output_embeddings_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(38, 24), nullable=True)
output_embeddings_batch_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(38, 24), nullable=True)

output_reasoning_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(38, 24), nullable=True)
output_reasoning_batch_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(38, 24), nullable=True)

output_image_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(38, 24), nullable=True)
output_image_batch_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(38, 24), nullable=True)

output_audio_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(38, 24), nullable=True)
output_audio_batch_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(38, 24), nullable=True)

# Usage:


# Cost
